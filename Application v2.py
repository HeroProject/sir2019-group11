import AbstractApplication as Base
from threading import Semaphore

class DialogFlowSampleApplication(Base.AbstractApplication):
    def main(self):      
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.language = 'en-US'
        self.langLock.acquire()
        
        self.setDialogflowKey('test-agent-jpjots-d58ddb261ce0.json')
        self.setDialogflowAgent('test-agent-jpjots')
        peopledict = pickle.load(open('peopledict.txt', 'rb'))

        self.speechLock = Semaphore(0)
        name = self.ask_question('Hello, what is your name?', 'answer_name')

        if name not in people_dict.keys():
            people_dict[name] = Person(name)
        self.person = people_dict[name]
        
        if self.person.firstlesson:
            self.sayAnimated2('Nice to meet you ' + self.person.name + '!')
            self.firstlesson()
        else:  # not self.person.firstlesson:
            self.sayAnimated2('oh Hello ' + self.person.name + '. Nice to see you again!')
            self.startlesson()

            
    def sayAnimated2(self, string):
        '''
        Just to acquire a speechlock after saying something, to make sure that the lock isn't forgotten
        Input: string to say
        Output: None
        '''
        self.sayAnimated(string)
        self.speechLock.Acquire()
        
        
    def listen(self, context):
        '''
        Listens for a response, while acquiring the correct locks.
        Input: context as a string (corresponding to dialogflow contexts)
        Output: string of the given answer
        '''
        self.answer = None
        self.answerLock = Semaphore(0)
        
        self.setAudioContext(context)
        self.startListening()
        self.answerLock.acquire(timeout=5)
        self.stopListening()
        
        if not self.answer:
            self.answerLock.acquire(timeout=1)
        
        return self.answer
    
    
    def ask_question(self, question, context):
        '''
        Recursively keep asking the question if someone doesnt answer or if the correct answer isnt recognized.
        Input: string question and a string context (corresponding to dialogflow contexts)
        Output: string of the given answer
        '''
        self.sayAnimated2(question)
        answer = self.listen(context)
        
        print(f'Question: {question}, Answer: {answer}')
        
        if answer is not None:
            return answer
        else:
            self.respond('no response')
            self.ask_question(question, context)
    
    
    def ask_to_repeat(self, word):
        '''
        Asks to repeat a dutch word. Recursively keep asking the person to repeat 
        the word if there is no answer or if the answer is not recognized.
        Input: string of word in dutch
        Output: None (if the answer is correct the lesson continues to the next word)
        '''
        self.changelanguage()
        self.sayAnimated2(word)
        answer = self.listen(word)
        self.changelanguage()

        print(f'Word: {word}, Answer: {answer}')

        if answer == word:
            self.respond('correct')
            if hasattr(self, 'lesson'):
                self.lesson.correct_answer(word)
        elif answer:
            self.respond('again')
            self.ask_to_repeat(word)
        else:
            self.respond('no response')
            self.ask_to_repeat(word)
    
    
    def respond(self, type_):
        '''
        Responds in a certain way after getting an answer from the person.
        The exact response is randomly sampled from the possible responses fitting the response type.
        Input: string of type_ (options are 'correct', 'again', 'no response')
        Output: None
        '''
        options = {
            'correct': 
                    ['Well done!', 
                    'Excellent!', 
                    'You\'ve done a great job!', 
                    'Perfect!', 
                    'Great!', 
                    'Good job'],
            'again': 
                    ['Would you please try again?', 
                    'That doesn\'t sound correct. Please try again.', 
                    'Just try one more time.', 
                    'I\'m sorry, would you try again?'],
            'no response': 
                    ['Let\'s try that again. But you should answer this time.', 
                    'Don\'t ignore me!', 
                    'Could you respond next time?', 
                    'It\'s not nice to ignore me!']}
    
        self.sayAnimated2(sample(options[type_], 1)[0])
      
    
    def onRobotEvent(self, event):
        '''
        Standard function from the framework to release some locks on certain events.
        '''
        if event == 'LanguageChanged':
            self.langLock.release()
        elif event == 'TextDone':
            self.speechLock.release()
        elif event == 'GestureDone':
            self.gestureLock.release()

            
    def onAudioIntent(self, *args, intentName):
        '''
        Standard function from the framework. Remove the lock from the answer so a new anser can be obtained.
        '''
        if intentName and len(args) > 0:
            self.answer = args[0]
            self.answerLock.release()


    def changeLanguage(self):
        '''
        Changes the language of the robot to dutch if it was in english and the other way around.
        Input: None
        Output: None
        '''
        if self.language == 'en-US':
            self.langLock = Semaphore(0)
            self.setLanguage('nl-NL')
            self.langLock.acquire() 
            self.language = 'nl-NL'

        else:  # self.language == 'nl-NL':
            self.langLock = Semaphore(0)
            self.setLanguage('en-US')
            self.langLock.acquire()
            self.language = 'en-US'
            self.sayAnimated2('Back to english')

            
    def firstlesson(self):
        '''
        First introductionary lesson where some basic things will be discussed. 
        Also updates the database (people_dict) for new people.
        Input: None
        Output: None
        '''
        self.sayAnimated2('Today we will start learning the Dutch language together. I would like to greet you in Dutch.')
        self.ask_to_repeat('goedenmiddag')

        # something something
        
        people_dict[self.person.name].firstlesson = False
        
        
    def startlesson(self):
        '''
        Ask the person what lesson they want to do. In the lesson random words 
        keep getting sampled untill all words have passed. If all words have been 
        repeated correctly the lesson is moved to learned_lessons in the databasefor the person.
        Input: None
        Output: None
        '''
        if len(self.person.lessons_to_learn) > 0:
            self.lesson = None

            self.sayAnimated2('What do you want to learn about today? Your options are')
            for lesson in self.person.lessons_to_learn:
                self.sayAnimated2(lesson.name)

            request = self.listen('lessons')

            for lesson in self.person.lessons_to_learn:
                if request.lower() == lesson.name.lower():
                    self.lesson = lesson

            if self.lesson is None:   
                self.lesson = sample(self.person.lessons_to_learn, 1)[0]

            for i in range(len(self.lesson.words_to_learn)):
                word = self.lesson.sample()
                self.sayAnimated2(f'The next word means {word.word}')
                self.ask_to_repeat(word.translation)

            self.person.update()
        else:
            self.sayAnimated2('It looks like you\'ve already completed all the lessons!')            

            
# Run the application
#sample = DialogFlowSampleApplication()
#sample.main()
#sample.stop()
