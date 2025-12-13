####### 

![Company Logo.bmp](media/image1.png){width="6.0in" height="1.5944444444444446in"}

**Design Document for:**

# Name of Game

**[One Liner, i.e. The Ultimate Racing Game]{.underline}**

"Something funny here!"™

All work Copyright ©1999 by Your Company Name

Written by Chris Taylor

Version \# 1.00

Sunday, July 05, 2015\
Table of Contents

Name of Game [1](#name-of-game)

Design History [5](#design-history)

Version 1.10 [5](#version-1.10)

Version 2.00 [5](#version-2.00)

Version 2.10 [5](#version-2.10)

Game Overview [6](#game-overview)

Philosophy [6](#philosophy)

Philosophical point #1 [6](#philosophical-point-1)

Philosophical point #2 [6](#philosophical-point-2)

Philosophical point #3 [6](#philosophical-point-3)

Common Questions [6](#common-questions)

What is the game? [6](#what-is-the-game)

Why create this game? [6](#why-create-this-game)

Where does the game take place? [6](#where-does-the-game-take-place)

What do I control? [6](#what-do-i-control)

How many characters do I control? [6](#how-many-characters-do-i-control)

What is the main focus? [6](#what-is-the-main-focus)

What's different? [7](#whats-different)

Feature Set [8](#feature-set)

General Features [8](#general-features)

Multi-player Features [8](#multiplayer-features)

Editor [8](#editor)

Game play [8](#gameplay)

The Game World [9](#the-game-world)

Overview [9](#overview)

World Feature #1 [9](#world-feature-1)

World Feature #2 [9](#world-feature-2)

The Physical World [9](#the-physical-world)

Overview [9](#overview-1)

Key Locations [9](#key-locations)

Travel [9](#travel)

Scale [9](#scale)

Objects [9](#objects)

Weather [9](#weather)

Day and Night [9](#day-and-night)

Time [10](#time)

Rendering System [10](#rendering-system)

Overview [10](#overview-2)

2D/3D Rendering [10](#d3d-rendering)

Camera [10](#camera)

Overview [10](#overview-3)

Camera Detail #1 [10](#camera-detail-1)

Camera Detail #2 [10](#camera-detail-2)

Game Engine [10](#game-engine)

Overview [10](#overview-4)

Game Engine Detail #1 [10](#game-engine-detail-1)

Water [10](#water)

Collision Detection [10](#collision-detection)

Lighting Models [11](#lighting-models)

Overview [11](#overview-5)

Lighting Model Detail #1 [11](#lighting-model-detail-1)

Lighting Model Detail #2 [11](#lighting-model-detail-2)

The World Layout [12](#the-world-layout)

Overview [12](#overview-6)

World Layout Detail #1 [12](#world-layout-detail-1)

World Layout Detail #2 [12](#world-layout-detail-2)

Game Characters [13](#game-characters)

Overview [13](#overview-7)

Creating a Character [13](#creating-a-character)

Enemies and Monsters [13](#enemies-and-monsters)

User Interface [14](#user-interface)

Overview [14](#overview-8)

User Interface Detail #1 [14](#user-interface-detail-1)

User Interface Detail #2 [14](#user-interface-detail-2)

Weapons [15](#weapons)

Overview [15](#overview-9)

Weapons Details #1 [15](#weapons-details-1)

Weapons Details #2 [15](#weapons-details-2)

Musical Scores and Sound Effects [16](#musical-scores-and-sound-effects)

Overview [16](#overview-10)

Red Book Audio [16](#red-book-audio)

3D Sound [16](#d-sound)

Sound Design [16](#sound-design)

Single Player Game [17](#single-player-game)

Overview [17](#overview-11)

Single Player Game Detail #1 [17](#single-player-game-detail-1)

Single Player Game Detail #2 [17](#single-player-game-detail-2)

Story [17](#story)

Hours of Game-play [17](#hours-of-gameplay)

Victory Conditions [17](#victory-conditions)

Multi-player Game [18](#multiplayer-game)

Overview [18](#overview-12)

Max Players [18](#max-players)

Servers [18](#servers)

Customization [18](#customization)

Internet [18](#internet)

Gaming Sites [18](#gaming-sites)

Persistence [18](#persistence)

Saving and Loading [18](#saving-and-loading)

Character Rendering [19](#character-rendering)

Overview [19](#overview-13)

Character Rendering Detail #1 [19](#character-rendering-detail-1)

Character Rendering Detail #2 [19](#character-rendering-detail-2)

World Editing [20](#world-editing)

Overview [20](#overview-14)

World Editing Detail #1 [20](#world-editing-detail-1)

World Editing Detail #2 [20](#world-editing-detail-2)

Extra Miscellaneous Stuff [21](#extra-miscellaneous-stuff)

Overview [21](#overview-15)

Junk I am working on... [21](#junk-i-am-working-on)

"XYZ Appendix" [22](#xyz-appendix)

"Objects Appendix" [22](#objects-appendix)

"User Interface Appendix" [22](#user-interface-appendix)

"Networking Appendix" [22](#networking-appendix)

"Character Rendering and Animation Appendix" [22](#character-rendering-and-animation-appendix)

"Story Appendix" [22](#story-appendix)

# Design History

This is a brief explanation of the history of this document.

In this paragraph describe to the reader what you are trying to achieve with the design history. It is possible that they don't know what this is for and you need to explain it to them.

## Version 1.10

Version 1.10 includes some tuning and tweaking that I did after making my initial pass at the design. Here is what I changed.

1.  I rewrote the section about what systems the game runs on.

2.  I incorporated feedback from the team into all parts of the design however no major changes were made.

3.  Just keep listing your changes like this.

## Version 2.00

Version 2.00 is the first version of the design where a major revision has been made now that much more is known about the game. After many hours of design, many decisions have been made. Most of these large design decisions are now reflected in this document.

Included in the changes are:

1.  Pairing down of the design scope. (Scope, not design)

2.  More detailed descriptions in many areas, specifically A, B and C.

3.  Story details.

4.  World layout and design.

## Version 2.10

Version 2.10 has several small changes over that of version 2.00. The key areas are in many of the appendixes.

Included in the changes are:

1.  Minor revisions throughout entire document.

2.  Added "User Interface Appendix".

3.  Added "Game Object Properties Appendix".

4.  Added concept sketch for world.

# Game Overview

## Philosophy

### Philosophical point #1

This game is trying to do this and that. Fundamentally I am trying to achieve something that has never been achieved before. Or. This game will not try and change the world. We are ripping off the competition so exactly that I can't believe it. The world will be shocked at how we are using an existing engine with new art.

### Philosophical point #2

Our game only runs on Compaq computers. The reason for this is such and such. We believe the world is coming to and end anyhow so what difference does it make?

### Philosophical point #3

When you create some of these overarching philosophical points about your design, say whatever you want. Also, feel free to change it to "My game design goals" or whatever you like to call it.

## Common Questions

### What is the game?

Describe the game is a paragraph. This is the answer to the most common question that you will be asked. What are you working on?

### Why create this game?

Why are you creating this game? Do you love 3D shooters? Do you think there is a hole in the market for Jell-O tossing midgets?

### Where does the game take place?

Describe the world that your game takes place in. Simple as that. Help frame it in the reader's mind by spending a few sentences on it here. You can go into lengthy detail later in a section solely dedicated to describing the world. Remember that we want to keep this part of the design light and readable.

### What do I control?

Describe what the player will control. You will be in charge of a band of rabid mutant fiddle players. If you want you can switch on the AI and turn it into a fish bowl simulation.

### How many characters do I control?

If this applies talk a little more about the control choices. Remember to add answers to questions that you think the reader will ask. This is totally dependent on your design.

### What is the main focus?

Now that we know where the game takes place and what the player controls. What are they supposed to achieve in this world? Angry fiddle players take over the U.N. building. Be careful not to add a bunch of salesmanship here. Your design wants to stay light and informative.

### What's different?

Tell them what is different from the games that are attempting this in the market right now. This question comes up a lot.

# Feature Set

## General Features

Huge world

Mutant fiddle players

3D graphics

32-bit color

## Multiplayer Features

Up to 10 million players

Easy to find a game

Easy to find your pal in huge world

Can chat over voice link

## Editor

Comes with world editor

Get levels from internet

Editor is super easy to use

## Gameplay

List stuff here that is key to the gameplay experience

List a lot of stuff here

Hey, if you got nothing here, is this game worth doing?

# The Game World

## Overview

Provide an overview to the game world.

## World Feature #1

This section is not supposed to be called world feature #1 but is supposed to be titled with some major thing about the world. This is where you break down what is so great about the game world into component pieces and describe each one.

## World Feature #2

Same thing here. Don't sell too hard. These features should be awesome and be selling the game on its own.

## The Physical World

### Overview

Describe an overview of the physical world. Then start talking about the components of the physical world below in each paragraph.

The following describes the key components of the physical world.

### Key Locations

Describe the key locations in the world here.

### Travel

Describe how the player moves characters around in the world.

### Scale

Describe the scale that you will use to represent the world. Scale is important!

### Objects

Describe the different objects that can be found in the world.

See the "Objects Appendix" for a list of all the objects found in the world.

### Weather

Describe what sort of weather will be found in the world, if any. Otherwise omit this section. Add sections that apply to your game design.

### Day and Night

Does your game have a day and night mode? If so, describe it here.

### Time

Describe the way time will work in your game or whatever will be used.

## Rendering System

### Overview

Give an overview of how your game will be rendered and then go into detail in the following paragraphs.

### 2D/3D Rendering

Describe what sort of 2D/3D rendering engine will be used.

## Camera

### Overview

Describe the way the camera will work and then go into details if the camera is very complicated in sub sections.

### Camera Detail #1

The camera will move around like this and that.

### Camera Detail #2

The camera will sometimes move like this in this special circumstance.

## Game Engine

### 

### Overview

Describe the game engine in general.

### Game Engine Detail #1

The game engine will keep track of everything in the world like such and such.

### Water

There will be water in the world that looks awesome and our game engine will handle it beautifully.

### Collision Detection

Our game engine handles collision detection really well. It uses the such and such technique and will be quite excellent. Can you see I am having a hard time making up stupid placeholder text here?

## Lighting Models

### Overview

Describe the lighting model you are going to use and then go into the different aspects of it below.

### Lighting Model Detail #1

We are using the xyz technique to light our world.

### Lighting Model Detail #2

We won't be lighting the eggplants in the game because they are purple.

# The World Layout

## Overview

Provide an overview here.

## World Layout Detail #1

## World Layout Detail #2

# Game Characters

## Overview

Over of what your characters are.

## Creating a Character

How you create or personalize your character.

## Enemies and Monsters

Describe enemies or monsters in the world or whomever the player is trying to defeat. Naturally this depends heavily on your game idea but generally games are about trying to kill something.\

# User Interface

## Overview

Provide some sort of an overview to your interface and same as all the previous sections, break down the components of the UI below.

## User Interface Detail #1

## User Interface Detail #2

# Weapons

## Overview

Overview of weapons used in game.

## Weapons Details #1

## Weapons Details #2

# Musical Scores and Sound Effects

### 

## Overview

This should probably be broken down into two sections but I think you get the point.

## Red Book Audio

If you are using Red Book then describe what your plan is here. If not, what are you using?

## 3D Sound

Talk about what sort of sound APIs you are going to use or not use as the case may be.

## Sound Design

Take a shot at what you are going to do for sound design at this early stage. Hey, good to let your reader know what you are thinking.

# Single-Player Game

## Overview

Describe the single-player game experience in a few sentences.

Here is a breakdown of the key components of the single player game.

## Single Player Game Detail #1

## Single Player Game Detail #2

## Story

Describe your story idea here and then refer them to an appendix or separate document which provides all the details on the story if it is really big.

## Hours of Gameplay

Talk about how long the single-player game experience is supposed to last or what your thoughts are at this point.

## Victory Conditions

How does the player win the single-player game?

# Multiplayer Game

## Overview

Describe how the multiplayer game will work in a few sentences and then go into details below.

## Max Players

Describe how many players can play at once or whatever.

## 

## Servers

Is your game client-server or peer-to-peer or whatever.

## Customization

Describe how the players can customize the multiplayer experience.

## Internet

Describe how your game will work over the internet.

## Gaming Sites

Describe what gaming sites you want to support and what technology you intend to use to achieve this. Perhaps Dplay or TCP/IP or whatever. It is probably a good idea to break the tech stuff out into a separate area, you decide.

## Persistence

Describe if your world is persistent or not.

## Saving and Loading

Explain how you can save a multiplayer game and then reload it. If you can or why this is not possible.

# Character Rendering

## Overview

Provide an overview as to how your characters will be rendered. You may have decided to include this elsewhere or break it out to provide more detail to a specific reader.

## Character Rendering Detail #1

## Character Rendering Detail #2

# World Editing

## Overview

Provide an overview about the world editor.

## World Editing Detail #1

## World Editing Detail #2

# Extra Miscellaneous Stuff

## Overview

Drop anything you are working on and don't have a good home for here.

## Junk I am working on...

Crazy idea #1

Crazy idea #2

#  "XYZ Appendix"

Provide a brief description of what this appendix is for and then get down to business and provide data to the reader.

Here are a few examples of some of the appendices in my latest design...

#  "Objects Appendix"

# "User Interface Appendix"

#  "Networking Appendix"

# "Character Rendering and Animation Appendix"

#  "Story Appendix"

Okay, that's it. I wanted to spend more time on this and really make it a great roadmap for putting a game design together. Unfortunately it would take a ton of time and that is something that we don't have enough of in this business. I think you get the idea anyhow. Also, don't get the impression that I think a design should provide the information in any particular order, this just happened to be the way it fell out of my head when I sat down. Change this template any way you want and if you feel you have improved on it, send it back to me and I can pass it out as an alternative to anyone that asks me in the future.

Good luck and all that!

Chris Taylor
