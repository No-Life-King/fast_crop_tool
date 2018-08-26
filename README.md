# Fast Crop Tool
A tool for manually cropping images down to a uniform size at a brisk pace.

<img src="https://raw.githubusercontent.com/No-Life-King/fast_crop_tool/master/user_guide_images/demo.gif"/>

<h2>How to Use Fast Crop Tool</h2>
Fast Crop Tool is a Python 3 script. To run it, you need to have Python 3 installed and execute the script from command prompt or set your operating system's default action for handling .py files to the Python interpreter and double click it. For more information on installing Python and running python scripts go to <a href="https://www.python.org/">python.org</a>. When you run the script, a configuration interface will be displayed. 

<img src="https://raw.githubusercontent.com/No-Life-King/fast_crop_tool/master/user_guide_images/configuration_interface.png"/>

Since Fast Crop Tool can delete images with a single button press, it is recommended that you make a copy of your folder of pictures so that you don't accidentally delete all of your original data. Select that copy as your source directory and then choose a destination directory that your new image crops can be saved to. The crop width and height can be changed to your desired size. Note that if crop selection exceeds the size of the image, a faulty crop will be made. Once your desired settings are correct, click the "Start Cropping" to start cropping. 

<h3>Controls</h3>
Fast Crop Tool uses one-button hotkey controls to help you quickly take crops of uniform size out of a large number of images. You may also take multiple crops out of the same image. The controls are as follows:

<b>D</b> - Advance to the next image. <br/>
<b>A</b> - Go back to the previous image. <br/>
<b>W</b> - Delete the current image and advance to the next image. <b>WARNING:</b> This will delete your image. <br/>
<b>Q</b> - Close out the window and quit Fast Crop Tool. <br/>
<b>Left-Click</b> - Make a crop where the green rectangle appears. The crop will be automatically saved to your destination folder. <br/>
<b>Scroll Wheel</b> - Increase/decrease the size of the crop rectangle. Note that crops will be scaled down to your desired crop size. <br/>

<h3>Supported File Types</h3>
The following image types are supported thanks to the <a href="https://opencv.org/">OpenCV Library</a>:
<ul>
  <li>.bmp</li>
  <li>.dib</li>
  <li>.jpeg</li>
  <li>.jpg</li>
  <li>.jpe</li>
  <li>.jp2</li>
  <li>.png</li>
  <li>.webp</li>
  <li>.pbm</li>
  <li>.pgm</li>
  <li>.ppm</li>
  <li>.sr</li>
  <li>.ras</li>
  <li>.tiff</li>
  <li>.tif</li>
</ul>

<h3>Results</h3>
Congratulations! You now have a bunch of manually cropped images.
<img src="https://raw.githubusercontent.com/No-Life-King/fast_crop_tool/master/user_guide_images/iris_crops.png"/>
