<h1 align="center">3D Model Icon Generator</h1>
<p align="center">
  <a href="https://github.com/JE323/3d-model-icon-generator/issues">Report Bug</a>
  ·
  <a href="https://github.com/JE323/3d-model-icon-generator/issues">Request Feature</a>
</p>

# Overview

3D Model Icon Generator generates icons when provided with a 3D model.

This uses Blender3D from the command line to generated images of models to be used as icons or thumbnails, the idea being this would be incorperated as part of an automated pipeline. Currently, .obj and .fbx model files are supported.

## Table of Contents

- [Overview](#overview)
- [Table of Contents](#table-of-contents)
- [1 - Installation](#1---installation)
  - [1.1 - Compatibility](#11---compatibility)
- [2 - Getting Started](#2---getting-started)
  - [2.1 - Install Blender 3D](#21---install-blender-3d)
  - [2.2 - Setup](#22---setup)
  - [2.3 - Configuration](#23---configuration)
- [3 - Usage](#3---usage)
  - [3.1 - Running](#31---running)
  - [3.2 - Customisation](#32---customisation)
- [4 - About](#4---about)
  - [4.1 - Versioning](#41---versioning)
  - [4.2 - Roadmap](42---roadmap)
  - [4.3 - Contributing](#43---contributing)
- [5 - License](#5---license)
- [6 - Acknowledgments](#6---acknowledgments)

## [1 - Installation](#table-of-contents)

### [1.1 - Compatibility](#table-of-contents)

This tool was tested with Blender 3D 2.79b.

For releases, please refer to the [**Release**](https://github.com/JE323/3d-model-icon-generator/releases) page.

## [2 - Getting Started](#table-of-contents)

### [2.1 - Install Blender 3D](#table-of-contents)
 
Follow the instructions provided by Blender3D for how to install the software. https://docs.blender.org/manual/en/dev/getting_started/index.html
Please note this package is currently only tested with Blender 3D 2.79b and is expected to not function with 2.8 onwards due to the major API changes that were made.

### [2.2 - Setup](#table-of-contents)
Download the github package.

```
git clone https://github.com/JE323/3d-model-icon-generator.git
```

### [2.3 - Configuration](#table-of-contents)
Configure the .json configuration file in `Processes\RenderFromPreconfigured\processSettings.json`

| Setting | Description | Example |
| ------- | ----------- | ------- |
| blenderLocation | Location of Blender installed on your computer | C:\\Program Files\\Blender Foundation\\blender-2.79b-windows64\\blender.exe |
| scriptLocation | Location of the python script to run within blender. As a minimum this should import the object and setup the camera location as templated within this project. Any render settings should be set within the render file. | generateIcon.py |
| logLocation | The directory location of where to store the generated log files. | \\Logs |
| renderFile | The location of the blender file `.blend` to use as the base render file. | \\renderScene.blend  |

## [3 - Usage](#table-of-contents)

### [3.1 - Running](#table-of-contents)

If everything has been following in [Getting Started](#2---getting-started) then the following command should generate an icon of the nut example model provided in this repositary.

Open a powershell terminal and navigate to the `Processes\RenderFromPreconfigured` folder within your git cloned folder.

Then run:
```
.\triggerRender.ps1 -file "..\..\ExampleObjects\nut.fbx" -output "..\..\Output\"
```

### [3.2 - Customisation](#table-of-contents)

There are two ways of configurating this package:
1. Custominsation of the render file. This is done within the blender file itself. For example, lighting or the background color.
2. Custominsation of the model within blender. This is done within the python script. For example, adding modifiers to the model or generating a wireframe instead of the solid mesh.

## [4 - About](#table-of-contents)

### [4.1 - Versioning](#table-of-contents)

This project uses [SemVer](http://semver.org/) for versioning. For releases, please refer to the [**Release**](https://github.com/JE323/3d-model-icon-generator/releases) page.

### [4.2 - Roadmap](#table-of-contents)

See the [open issues](https://github.com/JE323/3d-model-icon-generator/issues) for a list of proposed features (and known issues).

### [4.3 - Contributing](#table-of-contents)

If you would like to contribute please get in touch first with the functionality you would like to add with a short description of the new feature or bug/issue you would like to fix.

The list of contributors who have contributed can be found [here](https://github.com/JE323/3d-model-icon-generator/contributors).

## [5 - License](#table-of-contents)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use these files except in compliance with the License. See the [LICENSE.md](LICENSE.md) file for details.

## [6 - Acknowledgments](#table-of-contents)

Thanks to the team at Blender Foundation who produce Blender3D for the great work they do!
