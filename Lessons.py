import copy
from random import sample

class Word:
    def __init__(self, word, translation, sentence = None, sentence_translation = None):
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
            return sample(self.words_to_learn, 1)[0]
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