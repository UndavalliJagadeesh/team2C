from Detector import *
from Translate import *

import streamlit as st
# from streamlit_option_menu import option_menu

modelFile = 'efficientdet_d1_coco17_tpu-32.tar.gz'
modelURL = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/' + modelFile
classFile = 'coco.names'
threshold = 0.5
# API_KEY = '471b0e0033ab103162ac'
selected_language = None

detector = Detector()
translate = Translate()

detector.readClasses(classFile)
detector.downloadModel(modelURL)
detector.loadModel()


def capture():
    pass


def main():
    st.title("Foreign Language Learning through Object Detection using ANN")

    # selected = option_menu(
    #     menu_title=None,
    #     options=['Home', 'Detector'],
    #     icons=['house', 'search'],
    #     menu_icon='cast',
    #     default_index=0,
    #     orientation='horizontal'
    # )
    #
    # if selected == 'Home':
    #     st.write('In Development')
    #
    # elif selected == 'Detector':
    language_options = ['Afrikaans', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Azerbaijani', 'Basque',
                        'Belarusian',
                        'Bengali', 'Bosnian', 'Bulgarian', 'Catalan', 'Croatian', 'Czech', 'Danish', 'Dutch',
                        'English',
                        'Esperanto', 'Estonian', 'Filipino', 'Finnish', 'French', 'Galician', 'Georgian', 'German',
                        'Greek', 'Gujarati', 'Hebrew', 'Hindi', 'Hungarian', 'Icelandic', 'Indonesian', 'Irish',
                        'Italian',
                        'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Korean', 'Latin', 'Latvian', 'Lithuanian',
                        'Macedonian',
                        'Malay', 'Malayalam', 'Maltese', 'Marathi', 'Mongolian', 'Nepali', 'Norwegian', 'Persian',
                        'Polish',
                        'Portuguese', 'Punjabi', 'Romanian', 'Russian', 'Serbian', 'Sinhalese', 'Slovak',
                        'Slovenian',
                        'Spanish', 'Swahili', 'Swedish', 'Tamil', 'Telugu', 'Thai', 'Turkish', 'Ukrainian', 'Urdu',
                        'Uzbek', 'Vietnamese', 'Welsh', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu']

    col1, col2 = st.columns(2)
    with col1:
        st.text("Choose your language : ")
    with col2:
        selected_language = col2.selectbox(' ', language_options)
        translate.target_language = selected_language

    uploadedImage = st.file_uploader("Upload the image", type=['jpeg'])

    st.markdown("<h1 style='text-align: center; color: red;'>OR</h1>", unsafe_allow_html=True)

    capturedImage = st.camera_input("Capture")

    if uploadedImage:
        image = uploadedImage
    else:
        image = capturedImage

    if image:
        bytes_data = image.getvalue()
        image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image_with_bounding_boxes = detector.createBoundingBox(image, threshold)
        st.image(image_with_bounding_boxes)

        detected_objects = detector.detectedObjects
        st.text('Recognized objects :')
        for i in detected_objects:
            st.text(i)

        st.text('The detected object(s) in ' + selected_language + ' is(are) called :')
        for i in detected_objects:
            text, audio = st.columns(2)
            with text:
                st.text(i + ' - ' + translate.translate(i))
            with audio:
                audio_file = open('translated_audio.mp3', 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')


if __name__ == "__main__":
    main()
