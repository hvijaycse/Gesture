# Gesture

This gesture module is used to operate the system [ currently only mouse] with the __hand gesture__ input from webcam or a video.

As this module uses mediapipe library this can be easily run on CPU not requiring graphic card.

---

## 1 Get the code

 To get the code of this repo there are two methods

- Execute the  command  `git clone https://github.com/hvijaycse/Gesture` if you have [git CLI](https://git-scm.com/downloads) installed.

- Download the zip of this repo using this [link.](https://github.com/hvijaycse/Gesture/archive/refs/heads/main.zip)

---

## 2 Installation

1. First create a virtual enviroments for python3.7.10

    - I suggest [anaconda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands) step 3 in this

    - or you can also use [venv](https://docs.python.org/3/library/venv.html)
  
2. Activate the enviroment.

3. Install all the libraries required for this module by running the command <br> `pip install -r requirements.txt`

---

## 3 Running

### After Installation is complete.

1. Update the __*config.json*__ file.
 Set the value of __video_Source__ for video source input, if you intent to use webcam set it to **0**. I suggest [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_IN&gl=US) it provide better resolution then normal webcam.

2. Now to check if everything is working fine and the ML model is working well for your input run the python program `main.py` with `test` argument
<br>For eg: `python main.py test`
<br>Check if everything is working fine, all the hand gesture are getting detected properly.

3. If everything is working fine now you can now control you system by running the `main.py` program with `run` argument,
<br>For eg: `python main.py run`
<br>You should be able to control the mouse using your hand gesture.

---

## 4 Updating Gesture

### Now as you have tested the default gesture you can update the gestue according to yourself.

> The list of current gesture is **Idle, Cursor, Scroll, LeftMouseDown, LeftMouseDoubleClick, TaskView**.
>
> To update any of this gesture. Follow these steps. In the example I am going show the steps to update **Cursor** gesture.

1. Remove the datapoints of the current gesture use the program `data_handler.py` with remove argument.<br>For eg: If you want to remove **Cursor** gesture data point run the program with command `python data_handler.py remove Cursor`.

2. Now you can add your own gesture datapoints using the same program `data_handler.py` with add argument.<br>For eg: If you want to add **Cursor** gesture datapoints run the program with command `python data_handler.py add Cursor`<br>
A new window showing video and active area in frame will show up. Now show your hand gesture in the camera as soon as your hand will be detected. Move your hand to all the corners and all possible angles, this will generate good datapoints for your gesture.

3. *This step is optional*<br> You can visualize the gesture dataset that you just created using the `data_visualizer.ipynb` jupyter notebook. I have setup an Dimension reduction for 2d and 3d view. I hope you like it.
4. Now use the `model_trainer.ipynb` jupyter notebook to train a new ML model for your updated Gesture. Rather than a python program I created a notebook as it provide option to choose which ML algo to create and save the final model. If you don't have understanding of ML no need to worry, Just run the complete notebook, A good SVM model for your gesture dataset will be created and saved.

5. The final step.<br>Now just run the `main.py` program with test argument to make sure your gesture is getting detected properly and not getting conflicted with any other gesture. Once you verify everthing is good, now just run the `main.py` program with run argument and control your system with your own gesture.

<br>

**NOTE**
<br>
Most of the gestures utilize a landmark on your hand to perform certain operation, such as **Cursor** gesture tracks Middle Fingers tip to move the cursor on your system, If you want to update this and want any gesture to track any other landmark just Update the value corresponding to your gesture in *"Landmarks"* in `config.json` file.
<br>
<br>
Use this image for landmark names ![image.png](https://google.github.io/mediapipe/images/mobile/hand_landmarks.png)

---

## 5 Future

>I have created this module in such a way that it can be used with any mediapipe solution for gesture detection such as Pose, Hand, Face_Mesh, Holistic, etc.

>I have also created wrapper for mediapipe solutions as they required different methods and arguments to get the same output for different solutions such as plotting all the landmarks getting coordinate of a landmark etc.

> Now just import the solution from mediapipeSolution module and use them.

> Documentation for them is still remaining, I will add it in few days.

> These wrapper are compatible with the `model_trainer.ipynb` notebook and `main.py` program. Anyone with some knowledge can easily update the code and use them for pose gesture, face_mesh gesture and holistic gesture.

---

## 6 List of references

1. Google's amazing [mediapile](https://google.github.io/mediapipe/solutions/solutions.html) solution library.

2. This amazing tutorial on mediapipe [tutorial.](https://www.youtube.com/watch?v=01sAkU_NvOY)

3. Dimension Reduction and plotly using this [article](https://towardsdatascience.com/dimensionality-reduction-for-data-visualization-pca-vs-tsne-vs-umap-be4aa7b1cb29?gi=886aeece222f) on toward data science
