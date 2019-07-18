Documentation
============
The vector images for the open-simulation-interface documentation are provided in the .svg-format.

## Creating vector images
Objects such as roads, vehicles, signs, etc. that are embedded in the graphics are based on realistic high detailed 3D models.
The overall scene and 3D objects are modelled using the 3D modelling software [Blender](https://www.blender.org/).
The Freestyle SVG Exporter from Blender is used to convert the modelled 3D scene into vector graphics.

The Freestyle SVG Exporter add-on from Blender can be activated via the Render user settings. 
The GUI for the Exporter is located in the Render tab of the Properties Editor. After rendering, the exported .svg file is written to the output path.

For more information about Blender's Freestyle SVG Exporter add-on see:
 [docs.blender.org](https://docs.blender.org/manual/en/latest/render/freestyle/export_svg.html)

Following settings are used for exporting:
Freestyle SVG Export:
Frame, Round;
LineThickness = Absolute, 1.000px;

Freestyle Line Set: 
Visibility = Visible, 
Edgetype = Inclusive, 
Silhouette = true,
Border = true;

## Editing vector images

The exported 3D vector graphics can be opened and edited with any image editing program. (e.g. [Inkscape](https://inkscape.org/de/))
The vectors and labels are placed accordingly.
The graphics should generally be kept in a grayscale style.
RGBA code for grey: b3b3b3ff
