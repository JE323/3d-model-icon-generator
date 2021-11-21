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
  - [1.2 - Install Blender 3D](#12---install-blender-3d)
- [2 - Getting Started](#2---getting-started)
  - [2.1 - Setup](#21---setup)
  - [2.2 - Configuration](#22---configuration)
- [3 - Usage](#3---usage)
  - [3.1 - Running](#31---running)
    - [3.1.1 - Single Model](#311---single-model)
    - [3.1.2 - Multiple Models](#312---multiple-models)
  - [3.2 - Customisation](#32---customisation)
- [4 - About](#4---about)
  - [4.1 - Versioning](#41---versioning)
  - [4.2 - Roadmap](42---roadmap)
  - [4.3 - Contributing](#43---contributing)
- [5 - License](#5---license)
- [6 - Acknowledgments](#6---acknowledgments)

## [1 - Installation](#table-of-contents)

### [1.1 - Compatibility](#table-of-contents)

This tool was tested with Blender 3D 2.93. For previous version support please refer to the [**Release**](https://github.com/JE323/3d-model-icon-generator/releases) page.

### [1.2 - Install Blender 3D](#table-of-contents)
 
Follow the instructions provided by Blender3D for how to install the software. https://docs.blender.org/manual/en/dev/getting_started/index.html

## [2 - Getting Started](#table-of-contents)

### [2.1 - Setup](#table-of-contents)
Download the github package.

```
git clone https://github.com/JE323/3d-model-icon-generator.git
```

### [2.2 - Configuration](#table-of-contents)
For getting started this example uses the process called _RenderFromPreconfigured_ which can be found in the _Processes_ folder. The concept behind this is folders can be duplicated for complete flexibility of different processes that you wish to configure.

To test your first process, configure the .json configuration file in `Processes\RenderFromPreconfigured\processSettings.json`

| Setting | Description | Example |
| ------- | ----------- | ------- |
| blenderLocation | Location of Blender installed on your computer | C:\\Program Files\\Blender Foundation\\Blender 2.82\\blender.exe |
| scriptLocation | Location of the python script to run within blender. As a minimum this should import the object and setup the camera location as templated within this project. Any render settings should be set within the render file. | generateIcon.py |
| logLocation | The directory location of where to store the generated log files. This directory will autogenerate if it does not exist. | \\Logs |
| renderFile | The location of the blender file `.blend` to use as the base render file. | \\renderScene.blend  |

## [3 - Usage](#table-of-contents)

### [3.1 - Running](#table-of-contents)

After the setup in [Getting Started](#2---getting-started), the following commands are used to generate icons of the models you request. The examples here use the provided models in this repository for easy testing purposes.

| Setting | Description | Example |
| ------- | ----------- | ------- |
| -file / Model| The model file that you wish to have an icon generated for. | ..\\..\\ExampleObjects\\nut.fbx |
| -output / Folder / Directory (optional) | The output directory that you wish the icon to be generated to. If this is not specified then it will be saved to the same location as the model.  | ..\\..\\Output\\ |

These parameters works for both relative and absolute parameters.

#### [3.1.1 - Single Model](#table-of-contents)
Open a powershell terminal and navigate to the `Processes\RenderFromPreconfigured` folder within your cloned folder.

For a single model the script is called with ....

```
.\triggerRender.ps1 -file FILENAME
```
E.g.
```
.\triggerRender.ps1 -file "..\..\ExampleObjects\nut.fbx"
```

... or to specify the output location a second parameter can be used.

```
.\triggerRender.ps1 -file FILENAME -output DIRECTORY
```
E.g.
```
.\triggerRender.ps1 -file "..\..\ExampleObjects\nut.fbx" -output "..\..\Output\"
```

#### [3.1.2 - Multiple Models](#table-of-contents)
This same command can be easily extended for generating multiple model icons within a directory using the following pattern.
```
Get-ChildItem DIRECTORY | Foreach-Object { .\triggerRender.ps1 -Model $_.FullName }
```
E.g.
```
Get-ChildItem "..\..\ExampleObjects\" -Filter *.fbx | Foreach-Object { .\triggerRender.ps1 -Model $_.FullName }
```

For generating multiple files recursively from a directory:

```
Get-ChildItem "..\..\ExampleObjects\" -Filter *.fbx -Recurse | Foreach-Object { .\triggerRender.ps1 -Model $_.FullName }
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
