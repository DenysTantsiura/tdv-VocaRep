# ...! cd d:\mysenv\scripts\ .\activate.ps1
"""Vocabulary replenishment (Repetition of vocabulary) for learning a new language. Version 6.2.3


cd d:\mysenv\scripts
./activate

......."""
# from itertools import repeat
import os
from random import shuffle
import requests
from subprocess import call
import time


FILE_OF_WORDS = 'EnWords.txt'
FILE_OF_SCORES = 'EnWScores.txt'
FILE_REPORT = 'Summary result.txt'

AUDIO_FILE_CATEGORIES = ['', '_1', '_2', '_3', ]

BEGINNING = 'Okay, let\'s do it!'
FAREWELL = 'Bye! See you next time.'
GIVE_UP = 'I see it\'s hard for you...'
GREETING = 'Welcome!'
INVALIDE_COMMAND = 'Invalid command. Please try again.'
MISTAKE = 'Incorrect!'


def check_file(path_name_file: str) -> str:
    """Checks if the file exists and checks if the filename is free if not.
        Return unoccupied name of file.

        Parameters:
            path_name_file (str): Is proposed name of file

        Returns:
            path_name_file (str): Unoccupied name of file
    """
    if os.path.isdir(path_name_file):
        while os.path.isdir(path_name_file):
            path_name_file = 'new_one_' + path_name_file

    return path_name_file


def generate_report(_, vocabulary: dict, file_report: str, *_a) -> tuple:
    """Generate the report file and save it.

        Parameters:
            vocabulary(dict): Vocabulary dictionary
            file_report(str): Names(path) of file of report

        Returns:
            tuple(True(bool),): True if all okay
    """

    with open(file_report, 'w', encoding='utf-8-sig') as report_file:
        counter = 0
        for word in vocabulary['words_language_1']:
            line = f'''{word} - {vocabulary['words_language_2'][counter]}\n\t'''\
                f'''=attempts: {vocabulary['total_test'][counter]},\n\t'''\
                f'''successfully: {vocabulary['successful_results'][counter]}\n\n'''
            report_file.write(line)
            counter += 1

        print(f'File "{file_report}" generated successfully.')

    return True,


def save_result(vocabulary: dict, file_scores: str) -> tuple:
    """Write scores file. Return lists of words, scores.

        Parameters:
            vocabulary(dict): Vocabulary dictionary
            file_scores(str): Names(path) of scores file

        Returns:
            tuple(True(bool),): True if all okay
    """

    with open(file_scores, 'w', encoding='utf-8-sig') as scores_file:
        for counter, success in zip(vocabulary['total_test'], vocabulary['successful_results']):
            line = f'{counter} {success}\n'
            scores_file.write(line)

        print(f'File "{file_scores}" saves successfully.')

    return True,


def shuffle_the_indexes(word_count: int) -> list:
    """Shuffle the indexes of word list.

        Parameters:
            word_count (int): The number of words (len(words_list))

        Returns:
            Lisst of numers(indexes) in a mixed order
    """
    mix = [_ for _ in range(word_count)]
    shuffle(mix)
    shuffle(mix)

    return mix


def audio_hint_downloader(word: str, folder: str = 'English', language: str = 'en') -> bool:
    """
        Download the pronunciation of word (current_word) from a file in a certain language from
        Google Translate (GT) and save in audio file (.mp3).

        Parameters:
            word(str): Current word in certain language.
            folder(str): Directory(with path) for saving downloaded audio files. By default 'English'.
            language(str): language marking in the request. By default 'en'.
                (en - English; fr - French; es - Spanish;...)

        Returns:
            True or False, as a result of downloading and save it.
        """

    GOOGLE_WAY = 'https://translate.google.com/translate_tts?ie=UTF-&&client=tw-ob&tl='
    complete_link = f'{GOOGLE_WAY}{language}&q={word}'

    try:
        response = requests.get(complete_link)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else when trying download.", err)

    if not response:
        return False

    try:
        if folder:
            open(f'{folder}\\{word}.mp3', 'wb').write(
                response.content)  # need fixing '\\'
        else:
            open(f'{word}.mp3', 'wb').write(response.content)
    except IOError as pc_error:
        print(f'Sorry, but a hardware error has occurred'
              f'({pc_error}) while writing the file: {word}.mp3')
        return False
    except Exception as err:
        print("OOps: Something Else when trying save audio file.", err)
        return False

    return True


def play_the_audio_hint(current_word: str, repetitions: int = 1) -> None:
    """Play the audio hint few("repetitions") times for current word, if available.
        Needs: from subprocess import call.

        Parameters:
            current_word(str): Vocabulary word in 1st language.
            # watch in folder 'language_audio_hints'('English' for example), 
            # find and play 'current_word'.mp3

        Returns:
            None
    """
    if not os.path.isfile(f'C:\\Program Files\\VideoLAN\VLC\\vlc.exe'):
        return

    for sound_mark in AUDIO_FILE_CATEGORIES:
        if os.path.isfile(f'English\\{current_word}{sound_mark}.mp3'):
            for _ in range(repetitions):
                call(['C:\\Program Files\\VideoLAN\VLC\\vlc', '--play-and-exit',
                     f'English\\{current_word}{sound_mark}.mp3'])
        elif sound_mark == AUDIO_FILE_CATEGORIES[0]:
            play_the_audio_hint(current_word) if audio_hint_downloader(
                current_word) else None


def get_user_answer(message: str) -> str or bool:
    """Get the user's answer and return it if it exists."""
    print(message) if message else None
    try:
        user_answer = input()

    except IOError as e:
        errno, strerror = e.args
        print('I/O error({0}): {1}'.format(errno, strerror))
        return False

    if not user_answer:
        print('Unknown selection.\n')
        return False

    return user_answer


def check_user_answer(current_word: str, user_answer: str) -> bool:
    """Checking the correct spelling current word, with audio prompts if available.
        If the first letter of the word (phrase) is in upper case, then it is 
        necessary to adhere to the input case.
        Additionally, if "r" is entered(s) - an audio-hint is played if its available.

        Parameters:
            current_word(str): current word in language-1.
            user_answer(str): user answer in language-1.

        Returns:
            verdict: True or False of user response.
    """
    while user_answer == 'r':
        play_the_audio_hint(current_word)
        user_answer = get_user_answer('')

    if current_word[0].isupper() and user_answer == current_word:
        verdict = True

    elif user_answer.lower() == current_word.lower():
        verdict = True

    else:
        play_the_audio_hint(MISTAKE)
        time.sleep(2)
        verdict = False

    play_the_audio_hint(current_word, 2)

    return verdict


def calculate_the_time(start_time, end_time) -> time:
    """Calculate the time interval. Return value."""
    time_delta = end_time - start_time
    if time_delta < 60:
        return f'{int(time_delta)}s'
    elif time_delta < 60 * 60:
        return f'{int(time_delta//60)}m {int(time_delta%60)}s'
    elif time_delta < 60 * 60 * 24:
        return f'{int(time_delta//3600)}h {int(time_delta%3600)}m'
    else:
        return 'Are you alive?'


def repetition(_, vocabulary: dict, file_report: str, file_scores: str, repetition_limit: int) -> tuple:
    """Checking the correct spelling of each word in mix order, with audio prompts if available.
        And saves results in memory and scores file. 

        Parameters:
            vocabulary(dict): Vocabulary dictionary
            file_report(str): Names(path) of file of report (Not needed at the moment)
            file_scores(str): Names(path) of file of scores to fix the results in file.
            repetition_limit(int): for limitation of training repetition.

        Returns:
            tuple('training results', vocabulary): to fix the results in memory.
    """
    mixed_order = shuffle_the_indexes(len(vocabulary['words_language_1']))

    print('Okay, let\'s start.')
    play_the_audio_hint(BEGINNING)
    print('Enter "r" to repeat audio-hint.')

    start_repetition = time.time()

    while mixed_order:

        current_word_index = mixed_order.pop(0)

        if vocabulary['successful_results'][current_word_index] >= repetition_limit:
            continue

        elif vocabulary['total_test'][current_word_index] < 2:
            play_the_audio_hint(
                vocabulary['words_language_1'][current_word_index])

        user_answer = get_user_answer(
            f'''\n{vocabulary['words_language_2'][current_word_index]}:''')

        if user_answer == '4' or user_answer is False:
            break

        elif check_user_answer(vocabulary['words_language_1'][current_word_index], user_answer):
            vocabulary['successful_results'][current_word_index] += 1
            vocabulary['total_test'][current_word_index] += 1

        else:
            while user_answer != '4':

                play_the_audio_hint(
                    vocabulary['words_language_1'][current_word_index])
                user_answer = get_user_answer(
                    f'''Incorrect!, correct:\n {vocabulary['words_language_1'][current_word_index]}\nTry!:\n''')

                if user_answer == '4':
                    continue

                if check_user_answer(vocabulary['words_language_1'][current_word_index], user_answer):
                    print('Ok\n')
                    break

            else:
                print(f'{GIVE_UP}\n')
                play_the_audio_hint(GIVE_UP)
                break

    print('The training took:', calculate_the_time(
        start_repetition, time.time()))

    save_result(vocabulary, file_scores)

    return 'training results', vocabulary


def set_a_repeat_limit(user_command: list, *_) -> tuple:
    """Check a repetition limit for each word. Return the result for limitation.

        Parameters:
            user_command (list)

        Returns:
            True or False, and integer - limit
    """
    if len(user_command) > 1:
        limit = user_command[1]

    else:
        print('No parameter entered. Limit set as 3.')
        return 'set limit', 3

    try:
        limit = int(limit)

    except ValueError:
        print('Invalid limit. Must be an integer number between 1 and 100 (recomended 10).')
        return 'Error', 0

    if limit > 100 or limit < 1:
        limit = 10
        print('Limit must be between 1 and 100.')

    print(f'Limit set as {limit}.')

    return 'set limit', limit


MAIN_MENU = {
    '1': generate_report,
    'generate': generate_report,
    '2': repetition,
    'continue': repetition,
    '3': set_a_repeat_limit,
    'set': set_a_repeat_limit,
    '4': lambda *_: (None,),
    'exit': lambda *_: (None,),
}


def get_user_command() -> list or bool:
    """Get the user's choice and return it if it exists."""
    try:
        user_menu_selection = input('Enter your choice: ').lower().split(' ')

    except IOError as e:
        errno, strerror = e.args
        print('I/O error({0}): {1}'.format(errno, strerror))
        return False

    if not user_menu_selection:
        print('Unknown selection.\n')
        return False

    return user_menu_selection


def create_a_vocabulary_dictionary(vocabulary: dict, vocabulary_file: str, scores_file: str) -> dict:
    """Create a vocabulary dictionary from file of words. And return it."""
    with open(vocabulary_file, encoding='utf-8-sig') as file_of_words:
        for line in file_of_words:
            if len(line) > 2:
                line = line.rstrip().split(' - ')
                vocabulary['words_language_1'].append(line[0])
                vocabulary['words_language_2'].append(line[1])

    word_count = len(vocabulary['words_language_1'])

    if os.path.isfile(scores_file):
        with open(scores_file, encoding='utf-8-sig') as file_of_scores:
            for line in file_of_scores:
                if len(line) > 2 and len(vocabulary['total_test']) < word_count:
                    line = line.rstrip().split(' ')

                    try:
                        line[0] = int(line[0])
                    except:
                        line[0] = 0

                    try:
                        line[1] = int(line[1])
                    except:
                        line[1] = 0

                    vocabulary['total_test'].append(line[0])
                    vocabulary['successful_results'].append(line[1])

    else:
        vocabulary['total_test'] = [0 for _ in range(word_count)]
        vocabulary['successful_results'] = [0 for _ in range(word_count)]

    while len(vocabulary['total_test']) < word_count:
        vocabulary['total_test'].append(0)
        vocabulary['successful_results'].append(0)

    return vocabulary


def main():
    """Vocabulary replenishment (Repetition of vocabulary) for learning a new language."""
    vocabulary = {
        'words_language_1': [],
        'words_language_2': [],
        'total_test': [],
        'successful_results': [],
    }

    limit = 5  # default repetition limit for each word

    name_file_words = check_file(FILE_OF_WORDS)

    if not os.path.isfile(name_file_words):
        input('The source word file was not found! \nEnter to exit...')
        quit()

    name_file_scores = check_file(FILE_OF_SCORES)
    name_file_report = check_file(FILE_REPORT)
    vocabulary = create_a_vocabulary_dictionary(
        vocabulary, name_file_words, name_file_scores)

    # PAF!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    play_the_audio_hint(GREETING)
    while True:
        print('Welcome to the simple program to vocabulary replenishment of any language(English) words...')
        print('\nMenu: \n    1 - generate last results; \n    2 - continue learning; \
            \n    3 - set reminder limit; \n    4 - exit;\n')

        user_menu_selection = get_user_command()

        if not isinstance(user_menu_selection, list):
            continue

        action = MAIN_MENU.get(user_menu_selection[0], None)

        if not action:
            print(INVALIDE_COMMAND)
            play_the_audio_hint(INVALIDE_COMMAND)
            continue

        result = action(user_menu_selection, vocabulary,
                        name_file_report, name_file_scores, limit)

        if result[0] == 'set limit':
            limit = result[1]

        elif result[0] == 'training results':
            vocabulary = result[1]

        elif result[0] is None:
            print(FAREWELL)
            play_the_audio_hint(FAREWELL)
            break


if __name__ == '__main__':
    main()
