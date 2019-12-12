import AbstractApplication as Base
from threading import Semaphore
import copy
from random import sample
import pickle
import random


class Word:
    def __init__(self, word, translation, sentence=None, sentence_translation=None):
        self.word = word
        self.translation = translation
        self.sentence = sentence
        self.sentence_translation = sentence_translation


class Lesson:
    def __init__(self, name, words):
        self.name = name
        self.words_to_learn = words
        self.learned_words = []

    def append(self, word):
        '''
        Append a word or words to a lesson.
        Input: Instance of the class Word, or list of instances of the class Word
        Output: None
        '''

        if type(word) == list:
            self.words_to_learn.extend(word)
        else:
            self.words_to_learn.append(word)

    def sample(self):
        '''
        Sample from a new word from the words that are not yet learned.
        Input: None
        Output: Instance of the class Word
        '''
        if len(self.words_to_learn) > 0:
            return random.sample(self.words_to_learn, 1)[0]
        else:
            print('All words are learned')
            return

    def get(self, aword):
        '''
        Get a word from the words that are not yet learned.
        Input: English or Dutch word to learn as a string
        Output: Insance of the class Word corresponding to the word
        you requested iff the word is part of the lesson and not yet learned
        '''
        for word in self.words_to_learn:
            if (aword.lower() == word.word.lower()) or (aword.lower() == word.translation.lower()):
                return word

        print('Word is either already learned or is not part of this lesson.')

    def correct_answer(self, word):
        '''
        Call when a word is correctly learned. This function removes
        the word from the words to learn and adds it to the learned words.
        Input: Instance of the class Word or the english word as string
        Output: None
        '''
        if word in self.words_to_learn:
            self.words_to_learn.remove(word)
            self.learned_words.append(word)
        elif type(word) == str:
            self.learned_words.append(self.get(word))
            self.words_to_learn.remove(self.get(word))
        else:
            print('Word is either already learned or is not part of this lesson.')


class Person:
    def __init__(self, name):
        self.name = name
        self.firstlesson = True
        self.lessons_to_learn = copy.deepcopy(lessons)
        self.lessons_learned = []
        self.words_remembered = []

    def update(self):
        '''
        Check for every lesson if there are words left that arent learned yet.
        And updates the lessons_learned and lessons_to_learn properties.
        Input = None
        Output = None
        '''
        for lesson in self.lessons_to_learn:
            if len(lesson.words_to_learn) == 0:
                self.lessons_learned.append(lesson)
                self.lessons_to_learn.remove(lesson)


bike = Word('bicycle', 'fiets', 'I have a red bicycle', 'Ik heb een rode fiets')
car = Word('car', 'auto', 'A car has four wheels', 'Een auto heeft vier wielen')
train = Word('train', 'trein', 'The train leaves the station', 'De trein verlaat het station')
plane = Word('plane', 'vliegtuig', 'There is a plane in the air', 'Er is een vliegtuig in de lucht')
bus = Word('bus', 'bus', 'The bus drives through the city', 'De bus rijdt door de stad')
subway = Word('subway', 'metro', 'The subway is driving underground', 'De metro rijdt onder de grond')

mother = Word('mother', 'moeder', 'My mother is very smart', 'Mijn moeder is erg slim')
father = Word('father', 'vader', 'My father has a car', 'Mijn vader heeft een auto')
sister = Word('sister', 'zus', 'My sister is older than me', 'Mijn zus is ouder dan ik')
brother = Word('brother', 'broer', 'I play often with my brother', 'Ik speel vaak met mijn broer')
grandfather = Word('grandfather', 'opa', 'Every sunday, I go to my grandfather', 'Elke zondag, ga ik naar mijn opa')
grandmother = Word('grandmother', 'oma', 'My grandmother watches tv', 'Mijn oma kijkt tv')

cat = Word('cat', 'kat', 'The cat is hungry', 'De kat heeft honger')
dog = Word('dog', 'hond', 'The dog plays with a ball', 'De hond speelt met een bal')
gorilla = Word('gorilla', 'gorilla', 'There is a gorilla in the woods', 'Er is een gorilla in het bos')
mouse = Word('mouse', 'muis', 'The mouse eats some cheese', 'De muis eet wat kaas')
fish = Word('fish', 'vis', 'There is a fish in the water', 'Er is een vis in het water')
cow = Word('cow', 'koe', 'The cow does moooo', 'De koe doet moooo')
elephant = Word('elephant', 'olifant', 'The elephant eats peanuts', 'De olifant eet pinda’s')

transportation = Lesson('Transportation', [bike, car, train, plane, bus, subway])
family = Lesson('Family', [mother, father, sister, brother, grandfather, grandmother])
animals = Lesson('Animals', [cat, dog, gorilla, mouse, fish, cow, elephant])

lessons = [transportation, family, animals]


# pickle.dump({}, open('people_dict.txt', 'wb')) # run once to create a text file, then comment it out on any other run

class DialogFlowSampleApplication(Base.AbstractApplication):
    def main(self):      
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.language = 'en-US'
        self.langLock.acquire()
        
        self.setDialogflowKey('test-agent-jpjots-d58ddb261ce0.json')
        self.setDialogflowAgent('test-agent-jpjots')
        self.people_dict = pickle.load(open('people_dict.txt', 'rb'))

        self.speechLock = Semaphore(0)
        name = self.ask_question('Hello, what is your name?', 'answer_name')

        if name not in self.people_dict.keys():
            self.people_dict[name] = Person(name)
        self.person = self.people_dict[name]
        
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
        self.speechLock.acquire()
        
        
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
    
    
    def ask_question(self, question, context, switchlanguage = False):
        '''
        Recursively keep asking the question if someone doesnt answer or if the correct answer isnt recognized.
        Input: string question and a string context (corresponding to dialogflow contexts)
        Output: string of the given answer
        '''
        self.sayAnimated2(question)
        if switchlanguage:
            self.changelanguage()
            print(self.language)
        answer = self.listen(context)
        if switchlanguage:
            self.changelanguage()
            print(self.language)
        
        print(f'Question: {question}, Answer: {answer}')
        
        if answer:
            return answer
        else:
            self.respond('no response')
            self.ask_question(question, context, switchlanguage)
    
    
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
        self.counter += 1
        print('counter', self.counter)
        if answer == word:
            self.respond('correct')
            if hasattr(self, 'lesson'):
                self.lesson.correct_answer(word)
        elif answer and self.counter < 3:
            self.respond('again')
            self.ask_to_repeat(word)
        elif answer:
            self.sayAnimated2('Lets continue with the next word.')
        elif self.counter < 3:
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

        response = random.sample(options[type_], 1)[0]
        print(response)
        self.sayAnimated2(response)
      
    
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


    def changelanguage(self):
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

            
    def firstlesson(self):
        '''
        First introductionary lesson where some basic things will be discussed. 
        Also updates the database (people_dict) for new people.
        Input: None
        Output: None
        '''
        self.sayAnimated2('Today we will start learning the Dutch language together. I would like to greet you in Dutch.')
        self.sayAnimated2('Try to repeat after me')
        self.counter = 0
        self.ask_to_repeat('goedemiddag')
        self.sayAnimated2('This is it for our first intro lesson')
        answer = self.ask_question('Do you want to start the next lesson', 'Yesno')
        if answer == 'Yes':
            self.startlesson()
        else:
            self.sayAnimated2('See you next time. I hope you enjoyed our time together')
        # something something
        
        self.people_dict[self.person.name].firstlesson = False
        pickle.dump(self.people_dict, open('people_dict.txt', 'wb'))
    
    def recap_lesson(self, lesson):

        self.sayAnimated2('Let\'s start by going quickly through your previous lesson')
        
        words = random.sample(lesson.learned_words, 3)
        i = 0
        for word in words:
            options = [f'Can you tell me the dutch translation for {word.word}?',
                       f'How do you say {word.word} in Dutch?',
                       f'How about a word for {word.word} in Dutch?']

            answer = self.ask_question(options[i], word.translation, True)
            if answer.lower() == word.translation.lower():
                self.respond('correct')
                #self.person.words_remembered.append(word)
            elif answer:
                self.sayAnimated2(f'The correct translation of {word.word} is')
                self.changelanguage()
                self.sayAnimated2(word.translation)
                self.changelanguage()

            i -= -1
        #print(self.person.words_remembered)
            
        
        
    def startlesson(self):
        '''
        Ask the person what lesson they want to do. In the lesson random words 
        keep getting sampled untill all words have passed. If all words have been 
        repeated correctly the lesson is moved to learned_lessons in the databasefor the person.
        Input: None
        Output: None
        '''
        if len(self.person.lessons_learned) > 0:
            self.recap_lesson(self.person.lessons_learned[-1])
            
        if len(self.person.lessons_to_learn) > 0:
            self.lesson = None

            self.sayAnimated2('What do you want to learn about today? Your options are')
            for lesson in self.person.lessons_to_learn:
                self.sayAnimated2(lesson.name)

            request = self.listen('lessons')

            for lesson in self.person.lessons_to_learn:
                if request.lower() == lesson.name.lower():
                    self.lesson = lesson
                    self.sayAnimated2('Great, lets learn about' + lesson.name.lower())

            if self.lesson is None:   
                self.lesson = random.sample(self.person.lessons_to_learn, 1)[0]

            for i in range(len(self.lesson.words_to_learn)):
                word = self.lesson.sample()
                self.sayAnimated2(f'The next word means {word.word}')
                self.counter = 0
                self.ask_to_repeat(word.translation)
                
                if random.random() > .8:
                    self.sayAnimated2(f'Let\'s use {word.word} in a sentence')
                    self.sayAnimated2(word.sentence)
                    self.sayAnimated2('Dont get scared, you dont need to repeat after me')
                    self.changelanguage()
                    self.sayAnimated2(word.sentence_translation)
                    self.changelanguage()

            self.sayAnimated2('The lesson is done, your progress is saved')
            self.person.update()
            self.people_dict[self.person.name] = self.person
            pickle.dump(self.people_dict, open('people_dict.txt', 'wb'))
            answer = self.ask_question('Do you want to start the next lesson', 'Yesno')
            if answer == 'Yes':
                self.startlesson()
            else:
                self.sayAnimated2('See you next time. I hope you enjoyed our time together')
        else:
            self.sayAnimated2('It looks like you\'ve already completed all the lessons!')            

            
# Run the application
sample = DialogFlowSampleApplication()
sample.main()
sample.stop()
