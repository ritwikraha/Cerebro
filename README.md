# Cerebro
- - - - 
Imagine a machine so powerful that lets you visualise any brain wave and map the activity of any region of another person's mind. :brain: While all of this is a cake walk for Professor Charles Xavier, it proves to be quite an engineering challenge for the rest of us.

The field of human-machine interaction deals mostly with EEG Data. For various reasons, EEG Data is quite difficult to visualise clean and preprocess. Localising artifacts and identifying activity across brain regions remain a challenging task. 

The driving idea behind Cerebro is to easily visualise and plot brain activity from user entered EEG Data. Please note that the headset for this project is currently the [Emotiv 14 channel headset](https://www.emotiv.com/epoc/). :bar_chart:


![cerebro-gif](https://user-images.githubusercontent.com/44690292/106251928-9f4abd00-623b-11eb-9e9e-9e77ebc0a9ba.gif)

- - - - 
## Usage

* Clone the repository.
* Download and install the necessary packages from `requirement.txt`.
* Change the data files in the folder named `data`, only supports `.edf` files for now.
* Run `app.py`.

Or you can simply open the web app at [cerebrp-visualiser](https://cerebro-visualiser.herokuapp.com/) and enjoy the plots. If you want to tinker around without installing streamlit on your local computer, you can use the notebooks with google colab.

## Upcoming Updates

[] Provide support for data from other EEG headset.
[] Provide support for other formats of EEG Data.
[] Plot features like PSD and DE from selected channel
[x] Select a channel and frequency band to visualise the plot
[x] Show a topographical map from the EEG data 

- - - - 

## Acknowledgement

* Streamlit to heroku deployment learnt from [Krish Naik's tutorial](https://www.youtube.com/watch?v=5XnHlluw-Eo&feature=emb_title)
* Topography Map of Brain learnt from [Isuru Jayarathne's repository](https://github.com/ijmax/EEG-processing-python)
* EEG dataset of Fusion relaxation and concentration moods by [Ahmed Albasri](https://data.mendeley.com/datasets/8c26dn6c7w/1#__sid=js0)
* [Streamlit](https://www.streamlit.io/) a platform to create hassle free web apps with python.

- - - -
Professor Charles Xavier envisioned a world where science bridged barriers, while he is only fictional, his dream shouldn't be. Happy Coding. :smiley: