# colorthing
application to find color matching the average color in frame
made to be built into an apk package using buildozer.
Tested on arm64-v8a device
currently working: 'Match-mode'(camera+display matching colors-no button functionality)
TO CREATE APK PACKAGE:
buildozer android debug


PROJECT PLAN(- = Done, * = Not Done)

-match mode
    camera (works):
        -display camera view.
        * adjust camera image to crop image instead of changing proportions
        -find most commmon/mean color, save it.
        * explore other methods to find 'target' color 
        -cut out ROI
        * add functionality to adjust ROI size(UI)
        -blur non ROI
        -draw frame of ROI in 'target' color
    
    matcher (works-ish):
        - display rows of buttons
        - modify buttons color to be ether target color or matching colors
            column-wise: 
                -target color, with name of color theme
                -matching colors, with RGB values printed

        Button on click (not yet started)-
            * first of each row is never clickable
            If not selected, select:
                * draw outline on button/display changed state
                * 'gray out' all other buttons
                * deactivate all other buttons
                * switch to find-mode
                * Display some kind of similarity metric
            if selected:
                * remove outline of button
                * reset 'grayed out' buttons to original appearance
                * activate all buttons
                * switch back to 'match-mode'
                * remove metric display
find mode (not yet started)
    * create 'find-mode' to match a detected matching color
      to camera view
    * create option to 'check'(and uncheck)/if color is found- 
        *user decides if they are happy
        *'Permanent' indicator on button that color is found

Camera-modifier (not yet started):
    * UI to adjust color values in display
    * Add reset button.
    * make it a dropdown meny?
    * carousel of different color spaces? (BGR, HSV...)
