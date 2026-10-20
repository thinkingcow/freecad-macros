## Computer generated freecad 1.1 macros
I've been using Freecad to design objects to be 3D printed.  I find Freecad to be powerful but confusing, 
as it's model of operation often conflicts with mine.  I've asked Gemini to create macros for me that provide convenient 
operations for the projects I am building.  Sometimes they replicate  built-in capabilities, but in a form that makes more
sense to me; other times they are specific to a particular project.

I am keeping them here for my future use.  If anyone else finds them useful, then that is an added benefit.  In general,
If I need to modify a macro, I upload it to Gemini along with a  prompt for the modification.  So far, the only "by hand" 
modifications I've made are changes to the UI messages.

## Macros
- **allenkey**.  creates a 6-sided cylinder that can be subtracted from  a solid object to allow a standard Allen key to fit
            in the resultant cavity.  You specify the standard `key size`, `depth`, and `clearance`.
- **dup_around**.  Duplicates an object in a radial pattern around a
                  reference object.  You specify the number of duplicates,
                  which are placed uniformly in a circle around the
                  reference object, in the specified plane.  Changing a
                  property of the original object causes the equivalent
                  properties of the duplicated objects to stay in sync.
- **group_edit**.  You specify a collection of objects, based on a
                   substring that matches object labels.
                   Then specify a property name and value.  All matching
                   objects that have that property name have the value
                   changed accordingly.  A linked variable is created to
                   allow the chosen property for all matching objects
                   to be kept in sync.  The UI keeps track of the past
                   patterns, names, and values to make repetitive use
                   more convenient.
- **move_to**    Moves one object to the center of a reference object; the axis for centering (x, y, and/or z) can be specified.
- **spline**     Creates a cylinder with splines, suitable for cylindrical parts to be shoved into matching holes, the
                   splines adding friction for a tighter fit.  The splines
                   work on either the male or female (with subtraction)
                   sides the connection.
- **ellipse**    Creates an elliptical involute gear, with (optional) holes at the
                 center and foci
- **spiral**     Creates an archimedes spiral.  If another object is selected, it insets
                 the spiral into the face of the object to make it easy to print in a
                 contrasting color
- **chamfer_gears** adds chamfers to one or both sides of an fcgear generated planetary gear system
- **on_text** Writes text onto the face of the specified object.
- **fillet**  I can't figure out how to get the built-in fillet tool to support formulas for the
              fillet Radius.  This is a version of the Fillet tool that does.  It's
              not entirely general purpose, but works for me. It should work either in 
              the "part" or "part design" workshops
- **move_polar** Allows interactively moving an object in polar coordinates, using an
              linked VarSet.  The Varset can be safely removed as needed.
- **extract_to_varset**  A persistant version of "Group-Edit" that creates a varset
              of linked properties, allowing ongoing changes to linked properties
- **simpleEllipse** create a companion (e.g. similar) ellipse to the elliptical
             gear created with "ellipse"
- ** ovalGear** Create an oval gear suitable for 2 to rotate around their centers,
	     while meshing properly

## Realated resources
- **spur_gear_calculator.html**  A standalone html page that calculates the sizes of
             spur gears given the modulus and number of teeth.  Useful for back-of-the-envelope
             gear train calculations
- **InitGui.py** and **install_gitPython.py**
  Creates a Freecad module for integration with git.  Everytime a "save" is requested
  (and the file is in a git heirarchy), the user is prompted for a git-commit message, 
  and the change is checked in.  The **install** script can be used to install the 
  python library prerequisited into the appImage version of freecad.

## TODO
