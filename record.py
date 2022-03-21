# Current idea: Make user record audio first -> Then translation choice -> output
# Audio will be recorded through interaction (button or key press)
# MAYBE: Add TTS

import requests
import subprocess


# Function that handles microphone recording
def record_mic():
    # Ask user if they want to record until silence is detected or for a set amount of seconds.
    print("\n------------------------------------------------------------------------\n")
    print("\n\n1) Record until silence\n")
    print("2) Record for amount of seconds\n")
    mic_choice = input("Choice: ")

    # Depending on the choice, it will use SoX to record directly to a file named: 'mic_audio.flac'.
    if mic_choice == "1":
        input("Press enter to begin recording...\n")
        subprocess.run('rec mic_audio.flac silence 1 0.1 3% 1 3.0 3%', shell=True, check=True, executable='/bin/bash')
        audio_playback = input("\nPlay audio back? (Y/N): ")

        # If user wants to hear what they just recorded, play audio file.
        if audio_playback.upper() == "Y":
            subprocess.run('play mic_audio.flac', shell=True, check=True,
                           executable='/bin/bash')
        elif audio_playback.upper() == "N":
            print("\nSkipping audio playback...")

    # Set static amount of seconds to record for.
    elif mic_choice == "2":
        record_seconds = input("\nHow many seconds of recording?: ")
        input("Press enter to begin recording...\n")
        subprocess.run('rec mic_audio.flac trim 0 ' + record_seconds, shell=True, check=True, executable='/bin/bash')
        audio_playback = input("\nPlay audio back? (Y/N): ")

        # If user wants to hear what they just recorded, play audio file.
        if audio_playback.upper() == "Y":
            subprocess.run('play mic_audio.flac', shell=True, check=True,
                           executable='/bin/bash')
        elif audio_playback.upper() == "N":
            print("\nSkipping audio playback...")

    print("#$#$#$#$#$#$#$#$#$#$#$#$#$#")

    # Headers for the upcoming API call.
    stt_headers = {
        'Content-Type': 'audio/flac',
    }

    file_input = 'mic_audio.flac'

    print("\nLOADING....\n")

    # Speech to text audio input file
    stt_data = open(file_input, 'rb').read()
    audioresponse = requests.post(
        'https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/547a7142-216a-448c-9c5a-9ff698316466/v1/recognize',
        headers=stt_headers, data=stt_data, auth=('apikey', 'nHPSx1NUql-C6GDy8MPwChLxNlzXiMkNzNACrMRviEor'))

    # Set encoding for json output and serialize data.
    audioresponse.encoding = 'utf-8'
    audiojson = audioresponse.json()

    print("\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|\n")
    print("\n|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-\n")
    print("\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|\n")

    print("\n$$$$ TRANSCRIPT RESULTS $$$$\n")

    # Print the words detected by the speech-to-text API.
    print("Detected text --> " + audiojson["results"][0]["alternatives"][0]["transcript"])

    # Print transcription confidence.
    print("\nTranscription confidence: " + str(audiojson["results"][0]["alternatives"][0]["confidence"] * 100) + "%")

    # Write the speech-to-text to a file for later translation
    with open('transcript_out.txt', 'w+') as speechtext:
        speechtext.write(audiojson["results"][0]["alternatives"][0]["transcript"])


def text_input():
    input_text = input("\nTranslate: ")
    # Write the speech-to-text to a file for later translation
    with open('transcript_out.txt', 'w+') as speechtext:
        speechtext.write(input_text)


# For now, as a prototype, we will import audio. But, with pyaudio we should be able to stream/record data.
# https://cloud.ibm.com/docs/speech-to-text?topic=speech-to-text-input#timeouts
def import_audio():
    # speech to text headers
    stt_headers = {
        'Content-Type': 'audio/flac',
    }

    file_input = input("\nEnter filename (ex: audio-file.flac): ")

    # Set a default filename in case one is blank.
    if file_input == "":
        file_input = "audio-file.flac"

    audio_playback = input("\nPlay audio back? (Y/N): ")

    if audio_playback.upper() == "Y":
        subprocess.run('play ' + file_input, shell=True, check=True,
                       executable='/bin/bash')

    print("\nLOADING....\n")

    # Speech to text audio input file
    stt_data = open(file_input, 'rb').read()
    audioresponse = requests.post(
        'https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/547a7142-216a-448c-9c5a-9ff698316466/v1/recognize',
        headers=stt_headers, data=stt_data, auth=('apikey', 'nHPSx1NUql-C6GDy8MPwChLxNlzXiMkNzNACrMRviEor'))

    # Set encoding for json output and serialize data.
    audioresponse.encoding = 'utf-8'
    audiojson = audioresponse.json()

    print("\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|\n")
    print("\n|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-\n")
    print("\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|\n")

    print("\n$$$$ TRANSCRIPT RESULTS $$$$\n")

    # Print the words detected by the speech-to-text API.
    print("Detected text --> " + audiojson["results"][0]["alternatives"][0]["transcript"])

    # Print transcription confidence.
    print("\nTranscription confidence: " + str(audiojson["results"][0]["alternatives"][0]["confidence"] * 100) + "%")

    # Write the speech-to-text to a file for later translation
    with open('transcript_out.txt', 'w+') as speechtext:
        speechtext.write(audiojson["results"][0]["alternatives"][0]["transcript"])


def language_detection():
    ########                       ########
    #######                        #######
    ###### LANGUAGE DETECT SECTION ######

    # Language detection headers and CURL
    detectlang_headers = {
        'Content-Type': 'text/plain',
    }

    translate_params = (
        ('version', '2018-05-01'),
    )

    # Translate our streamed text file that was made by text-to-speech.
    translate_data = open('transcript_out.txt').read()

    # Send text file through API...
    detectlang_response = requests.post(
        'https://api.us-east.language-translator.watson.cloud.ibm.com/instances/38db0a04-d9a3-4ef8-9df2-59ede33bc939/v3/identify',
        headers=detectlang_headers, params=translate_params, data=translate_data,
        auth=('apikey', 'MxazkuoQCJhOyDoEZdgh669vtV6x0staGONvDttM_1J8'))

    detectlang_response.encoding = 'utf-8'

    # Serialize the response data
    detectlang_json = detectlang_response.json()

    # Print detected top language
    # If english, print that it is english.
    if detectlang_json["languages"][0]["language"] == 'en':
        print("\nDetected input language: English")
    else:
        # Else, just print the 2 letter abbreviation of the language.
        print("\nDetected input language: " + detectlang_json["languages"][0]["language"])

    # Print detected confidence in top language selection
    print("\nConfidence in top language detection: " + str(detectlang_json["languages"][0]["confidence"] * 100)[:-11] + "%")
    print("\n------------------------------------------------------------------------\n")

    # Just make a new variable for the detected language of the audio
    CURRENT_LANGUAGE = str(detectlang_json["languages"][0]["language"])

    # Initial language selection screen
    while True:
        print("Select language to translate to: \n")
        print("1) Spanish\n")
        print("2) French\n")
        print("3) Portuguese\n")
        print("4) German\n")
        print("5) Simplified Chinese\n")
        print("6) Japanese\n")
        print("7) English\n")
        print("-----------------------------")
        language_choice = input("\nChoice: ")

        # Do a check to see if current language == the language you are trying to translate to.
        # If so, deny this and repeat until valid choice.
        if CURRENT_LANGUAGE == "es" and language_choice == "1" or language_choice.upper() == "SPANISH":
            print("\nAudio is already in Spanish!\n\n\n")
            pass
        elif language_choice == "1" or language_choice.upper() == "SPANISH":
            translationlang = CURRENT_LANGUAGE + "-es"
            return translationlang
        elif CURRENT_LANGUAGE == "fr" and language_choice == "2" or language_choice.upper() == "FRENCH":
            print("\nAudio is already in French!\n\n\n")
            pass
        elif language_choice == "2" or language_choice.upper() == "FRENCH":
            translationlang = CURRENT_LANGUAGE + "-fr"
            return translationlang
        elif CURRENT_LANGUAGE == "pt" and language_choice == "3" or language_choice.upper() == "PORTUGUESE":
            print("\nAudio is already in Portuguese!\n\n\n")
            pass
        elif language_choice == "3" or language_choice.upper() == "PORTUGUESE":
            translationlang = CURRENT_LANGUAGE + "-pt"
            return translationlang
        elif CURRENT_LANGUAGE == "de" and language_choice == "4" or language_choice.upper() == "GERMAN":
            print("\nAudio is already in German!\n\n\n")
            pass
        elif language_choice == "4" or language_choice.upper() == "GERMAN":
            translationlang = CURRENT_LANGUAGE + "-de"
            return translationlang
        elif CURRENT_LANGUAGE == "zh" and language_choice == "5" or language_choice.upper() == "CHINESE" or language_choice.upper() == "SIMPLIFIED CHINESE":
            print("\nAudio is already in Chinese!\n\n\n")
            pass
        elif language_choice == "5" or language_choice.upper() == "CHINESE" or language_choice.upper() == "SIMPLIFIED CHINESE":
            translationlang = CURRENT_LANGUAGE + "-zh"
            return translationlang
        elif CURRENT_LANGUAGE == "ja" and language_choice == "6" or language_choice.upper() == "JAPANESE":
            print("\nAudio is already in Japanese!\n\n\n")
            pass
        elif language_choice == "6" or language_choice.upper() == "JAPANESE":
            translationlang = CURRENT_LANGUAGE + "-ja"
            return translationlang
        elif CURRENT_LANGUAGE == "en" and language_choice == "7" or language_choice.upper() == "ENGLISH":
            print("\nAudio is already in English!\n\n\n")
            pass
        elif language_choice == "7" or language_choice.upper() == "ENGLISH":
            translationlang = CURRENT_LANGUAGE + "-en"
            return translationlang
        else:
            print("\nInvalid choice... Restarting\n\n\n")


def translate(translationlang):
    ########                   ########
    #######                    #######
    ###### TRANSLATION SECTION ######

    # Translation API headers
    translate_headers = {
        'Content-Type': 'application/json',
    }

    translate_params = (
        ('version', '2018-05-01'),
    )

    # Translate to the translationlang variable language.
    translate_json_data = {
        'text': [
            open('transcript_out.txt').read(),
        ],
        'model_id': str(translationlang),
    }

    translate_response = requests.post(
        'https://api.us-east.language-translator.watson.cloud.ibm.com/instances/38db0a04-d9a3-4ef8-9df2-59ede33bc939/v3/translate',
        headers=translate_headers, params=translate_params, json=translate_json_data,
        auth=('apikey', 'MxazkuoQCJhOyDoEZdgh669vtV6x0staGONvDttM_1J8'))

    translate_response.encoding = 'utf-8'
    translate_json = translate_response.json()

    # Print only the translation
    print("Translated to: " + translationlang)
    print("\t\t\t|\n")
    print("\t\t\t|\n")
    print("\t\t\tV\n")
    print(translate_json["translations"][0]["translation"])
    #print(translate_json)
    print("\n-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|\n\n\n\n")
    input("Press enter to continue...\n")


# This is the main menu where you can select you input type.
# Input type 1: Audio input, file -> You can upload an audio file to have it translated.
# Input type 2: Audio input, mic -> You can record a short audio clip and have it translated.
# Input type 3: text -> Type to have text translated.
while True:
    print("""\n       _____      __               _______     __ __       _____      __   __    ______    __         _____      _______     __      _____      __   __   
      /\___/\    /\_\            /\_______)\  /_/\__/\    /\___/\    /_/\ /\_\  / ____/\  /\_\       /\___/\   /\_______)\  /\_\    ) ___ (    /_/\ /\_\  
     / / _ \ \   \/_/            \(___  __\/  ) ) ) ) )  / / _ \ \   ) ) \ ( (  ) ) __\/ ( ( (      / / _ \ \  \(___  __\/  \/_/   / /\_/\ \   ) ) \ ( (  
     \ \(_)/ /    /\_\             / / /     /_/ /_/_/   \ \(_)/ /  /_/   \ \_\  \ \ \    \ \_\     \ \(_)/ /    / / /       /\_\ / /_/ (_\ \ /_/   \ \_\ 
     / / _ \ \   / / /            ( ( (      \ \ \ \ \   / / _ \ \  \ \ \   / /  _\ \ \   / / /__   / / _ \ \   ( ( (       / / / \ \ )_/ / / \ \ \   / / 
    ( (_( )_) ) ( (_(              \ \ \      )_) ) \ \ ( (_( )_) )  )_) \ (_(  )____) ) ( (_____( ( (_( )_) )   \ \ \     ( (_(   \ \/_\/ /   )_) \ (_(  
     \/_/ \_\/   \/_/              /_/_/      \_\/ \_\/  \/_/ \_\/   \_\/ \/_/  \____\/   \/_____/  \/_/ \_\/    /_/_/      \/_/    )_____(    \_\/ \/_/  
                                                                                                                                                          """)

    print("\n- Robert")
    print("\n- Asmeret")
    print("\n- Fengnan")

    print("\n------------------------------------------------------------------------\n")
    print("\n1) Audio input [file]\n")
    print("2) Audio input [microphone]\n")
    print("3) text input\n")
    mediachoice = input("Choice: \n")

    # Depending on user choice, detection changes.
    if mediachoice == "1" or mediachoice.upper() == "FILE":
        # Run all functions on file.
        import_audio()
        translation_language = language_detection()
        translate(translation_language)
    elif mediachoice == "2" or mediachoice.upper() == "MICROPHONE" or mediachoice.upper() == "MIC":
        # Wait for user to press space to begin recording. Max 15 seconds.
        record_mic()
        translation_language = language_detection()
        translate(translation_language)
    elif mediachoice == "3" or mediachoice.upper() == "TEXT":
        # Ask user to type in some text and output the translation.
        text_input()
        translation_language = language_detection()
        translate(translation_language)
    elif mediachoice.upper() == "EXIT" or mediachoice.upper() == "QUIT":
        break
    else:
        print("INVALID INPUT\n\n\n")
