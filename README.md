# Audio Blog

App Link: https://imgaler.herokuapp.com/



## Key Features


* The CSS layout design. We tried our best to keep buttons of a audio in on the same horizontal line and make same bueatiful.
* Record Audio and Store the Audio. We use Javascript format to transfer data to flask sever.
* Audio Wave. Use javascript show the audio wave.



## Screenshots of Site

**[Add a screenshot of each key page (around 4)](https://stackoverflow.com/questions/10189356/how-to-add-screenshot-to-readmes-in-github-repository)
along with a very brief caption:**

![96c1943dcb5b1fd02ca913aa9c835be](https://user-images.githubusercontent.com/62827754/159841315-4627ef72-c8f1-4ff7-808b-f6cfbdb061ba.png)
This is main page. All users could view the public audios and also could search keywords in description of all audios for finding some related audios.


![微信图片编辑_20220323232413](https://user-images.githubusercontent.com/62827754/159841880-6f2a8772-3d9f-49d3-bf17-80635ee73a73.jpg)
This is personal page. Only registered users could access this page. Users could upload their audios to the server by selecting audio files from the local or recording their sounds from this page. They could set audio to be public or private. The personal search tag could search audios based on description.


## Mock-up 
Functions: 
- Post your audio blogs
- Content: Voices and short Description
- Voice to Letters（Simplify Content）
- Register and Unregister Users:
	1. Registered users can edit, post, delete and view the contents
	2. Unregistered users can only view the public contents

Users can choose whether they want to share the “Voice Post” publicly.




1. Home Page

Users can search for an audio blogs in the home page.

![index](https://user-images.githubusercontent.com/14122965/153987251-23615f8f-a012-4dc0-97a7-49c8046e643e.PNG)


2. Personal recordings

![personal](https://user-images.githubusercontent.com/14122965/153986508-d1a0c5e1-b0b2-4a9f-bc9b-d420c48b22eb.PNG)


3. Account | Login/Register

![account](https://user-images.githubusercontent.com/14122965/153986902-26e84a43-182c-45d5-80b6-33d7b23120ec.PNG)





## External Dependencies

**Document integrations with 3rd Party code or services here.


* Library or service name: description of use
* Auth0: We use auth0 for login.
* unpkg.com/wavesurfer.js(https://wavesurfer-js.org/): use it for displaying the sound waves.
