## Computer generated freecad 1.1 macros
I've been using Freecad to design objects to be 3D printed.  I find Freecad to be powerful but confusing, 
as it's model of operation often conflicts with mine.  I've asked Gemini to create macros for me that provide convenient 
operations for the projects I am building.  Sometimes they replicate  built-in capabilities, but in a form that makes more
sense to me; other times they are specific to a particular problem.

I am keeping them here for my future use.  If anyone else finds them useful, then that is an added benefit.  In general,
If I need to modify a macro, I upload it to Gemini along with a  prompt for the modification.  So far, the only "my hand" 
modifications I've made are changes to the UI messages.

## Macros
- **allenkey**.  creates a 6-sided cylinder that can be subtracted from  a solid object to allow a standard Allen key to fit
            in the resultant cavity.  You specify the standard `key size` , `depth`, and `clearance`.
- **dup_around**.  Duplicates an object in a radial pattern around a reference object.  You specify the number of duplicates,
                  which are placed uniformly in a circle around the reference object, in the specified plane.  Changing a property of the original
                  object causes the equivalent properties of the duplicated objects to stay in sync.
- **group_edit**.  You specify a collection of objects, based on a substring that matches object labels.
                   Then specify a property name and value.  All matching objects that have that property name have the value changed
                   accordingly.  A linked variable is created to allow the chosen property for all matching objects to be kept in sync.
                   The UI keeps track of the past patterns, names, and values to make repetitive use more convenient.
- **move_to**    Moves one object to the center of a reference object; the axis for centering (x, y, and/or z) can be specified.
- **spline**     Creates a cylinder with splines, suitable for cylindrical parts to be shoved into matching holes, the
                   splines adding friction for a tighter fit.  The splines work on either the male or female (with subtraction) sides
                   the connection.
- **ellipse**    Creates an elliptical involute gear.
