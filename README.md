# colorchooser
(android-targetting) kivy application to find color matching the average color in frame.<br /> 
made to be built into an apk package using buildozer.<br />
<br />
Tested on device:<br />
*arm64-v8a*<br />
<br/>
currently working:<br />
*camera (displaying and modification of frames works as intended)*<br />
*'Matcher (draws all buttons as indended. But no functionality)*<br />
<br />
TO CREATE APK PACKAGE:<br />
*buildozer android debug*<br />
<br />
<br />

    CURRENT PROJECT PLAN
    (- = Done, * = Not Done)

    match mode
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
            - use color detected by camera to create color themes
            * modify color theme creation/find alternative/better methods.
            (make it work for both dark and light colors, manage shadows/reflections...)
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
