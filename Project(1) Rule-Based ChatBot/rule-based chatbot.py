from nltk import word_tokenize
from nltk.stem import wordnet
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import random
import string
import warnings
import bs4 as bs
import urllib.request
import re
#nltk.download('punkt')
#nltk.download('wordnet')


warnings.filterwarnings("ignore")
synonyms = []
for syn in wordnet.synsets('hello'):
    for lem in syn.lemmas():
        Lem_name = re.sub(r'[[0-9]+\]','', lem.name())
        Lem_name = re.sub(r'\s+', ' ', lem.name())
        synonyms.append(Lem_name)

# Greetings and Synonyms
greeting_inputs = ["hey", "good morning", "good evening", "morning", "evening", "hi", "whatsup","hello there", "hi there", "hey there", "howdy", "greetings", "hola","hello"]

# Conversation Inputs
convo_inputs = ['how are you', 'how are you doing', 'you good', 'what are you up to', 'how is your day']

# Greeting Responses
greeting_responses = ['Hello! How can I help you?', 'Hey there! So what do you want to know?', 'Hi, you can ask me anything.', 'Hey! Wanna know about Football? Just ask away!']

# Conversation Responses
convo_responses = ['Great! What about you?', 'Getting bored at home :( How about you?', 'Not too shabby.']

# Conversation Replies by User
convo_replies = ['great', 'i am fine', 'fine', 'good', 'super', 'superb', 'super great', 'nice', 'not bad', 'okay']

# Additional Greetings, Responses, and Replies
greeting_inputs += ['good day', 'good afternoon']
greeting_responses += ['Good day! How can I assist you today?', 'Good afternoon! What can I help you with?']
convo_replies += ['not so good', 'feeling down', 'could be better', 'so-so', 'feeling alright']
# Previous code snippet
question_answers = {
    'what are you': 'I am bot, ro-bot :and my name is Raad',
    'who are you': 'I am bot, ro-bot :and my name is Raad',
    'what can you do': 'Answer questions regarding Football!',
    'what do you do': 'Answer questions regarding Football!'
}

#To generate our corpus, we will use the Fottball page on Wikipedia.

r_html = urllib.request.urlopen('https://en.wikipedia.org/wiki/Football')
r_html = r_html.read()

a_html = bs.BeautifulSoup(r_html, 'html.parser')

a_paragraphs = a_html.find_all('p')

a_text = ''

for p in a_paragraphs:
    a_text += p.text

a_text = a_text.lower()


#Take out all of the special characters and blank spaces from our text.
a_text = re.sub(r'\[[0-9]*\]', ' ', a_text)
a_text = re.sub(r'\s+', ' ', a_text)

#Because the cosine similarity of the user input will be compared with each phrase, we must break our text into sentences and words.
a_sentences = nltk.sent_tokenize(a_text)
a_words = nltk.word_tokenize(a_text)

#We need to provide helper functions that remove punctuation from user-input text and also lemmatize it.
lemmatizer = nltk.stem.WordNetLemmatizer()

def eliminate_punctuation(a_text):
    translator = str.maketrans(' ', ' ', string.punctuation)
    return a_text.translate(translator)

def lemmatizeing(text):
    def get_wordnet_pos(a_word):
        """Map POS tag to first character lemmatize() accepts"""
        tag = nltk.pos_tag([a_word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)

    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in tokens]
    return ' '.join(lemmatized_tokens)

def punc_remove(text):
    punctuations = r'!0-[16};:*"\\,∞./?0#88^&*_~111'  # Escaped special characters
    no_punct = ''
    for char in text:
        if char not in punctuations:
            no_punct += char
    return no_punct

def generate_greeting_response(hello):
    cleaned_hello = punc_remove(hello.lower())
    if cleaned_hello in greeting_inputs:
        return random.choice(greeting_responses)


# Method to generate a response to conversations
def generate_convo_response(text):
    cleaned_text = punc_remove(text.lower())
    if cleaned_text in convo_inputs:
        return random.choice(convo_responses)


# Method to generate answers to questions
def generate_answers(text):
    cleaned_text = punc_remove(text.lower())
    if cleaned_text in question_answers:
        return question_answers[cleaned_text]


#Answering User Inquiries
def create_a_response(user_input, get_processed_text=None):
   Raadrobo_response = ''
   a_sentences.append(user_input)
#After initializing the tfidfvectorizer, we convert all of the sentences in the corpus, as well as the input sentence, into their vectorized forms.
   word_vectorizer: TfidfVectorizer = TfidfVectorizer(tokenizer=get_processed_text, stop_words='english')
   all_word_vectors = word_vectorizer.fit_transform(a_sentences)
   #The cosine_similarity function is used to calculate the cosine similarity between the last item in the all_word_vectors list (which is actually the word vector for the user input because it was attached at the end) and the word vectors for all the sentences in the corpus.
   similar_vector_values = cosine_similarity(all_word_vectors[-1], all_word_vectors)
   #When sorting the list of cosine similarities, the second last item has the greatest resemblance to the user input, because the last item represents the user input itself.
   equivalent_sentence_number = similar_vector_values.argsort()[0][-2]

   matched_vector = similar_vector_values.flatten()
   matched_vector.sort()
   vector_matched = matched_vector[-2]

   if vector_matched == 0:
        Raadrobo_response = Raadrobo_response + "I am sorry, I could not understand you"
        return Raadrobo_response
   else:
        Raadrobo_response = Raadrobo_response + a_sentences[equivalent_sentence_number]
        return Raadrobo_response

#Chatting with the Chatbot
continue_chat = True

print('Hi! I am RaadRobo. You can ask me anything regarding Football and I shall try my best to answer them: ')

while continue_chat:
    user_input = input().lower()
    user_input = punc_remove(user_input)

    if user_input != 'bye':
        if user_input == 'thanks' or user_input == 'thank you very much' or user_input == "thank you":
            continue_chat = False
            print('RaadRobo: Not a problem! (And WELCOME! :D)')
        elif user_input in convo_replies:
            print('That\'s nice! How may I be of assistance?')
            continue
        else:
            if generate_greeting_response(user_input) is not None:
                print('RaadRobo: ' + generate_greeting_response(user_input))
            elif generate_convo_response(user_input) is not None:
                 print('RaadRobo: ' + generate_convo_response(user_input))
            elif  generate_answers(user_input)  is not None:
                  print('RaadRobo: ' + generate_answers(user_input))
            else:
                        print('RaadRobo: ', end='')
                        print(create_a_response(user_input))
                        a_sentences.remove(user_input)
    else:
        continue_chat = False
        print('RaadRobo: Goodbye! Have a great day!')
