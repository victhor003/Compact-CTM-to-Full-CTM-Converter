# Compact-CTM-to-Full-CTM-Converter
My first app, and a simple python program to convert optifine's compact CTM images to a full CTM. The program composes the images in the same order and way that optifine does it in-game, but because it's a full CTM there is less chance of the lighting engine to bug out. The main use for this program originally was to make it easier to prepare textures for the overlay_CTM method wich doesn't support compact_CTM natively.

How to use: 
1. Open the program.
2. In the input part, click "Search" and select a folder to pick the input from.
3. On the output part, click "Search" and select a folder to output the images to.
4. On the right panel, open the resolutions box and select the resolution of your files.
5. Click on the "Preview Button" button on the right panel to generate the images.
6. Once you are happy with the output, click the "Confirm" button of the right panel.
7. If you've done everything correctly, you will find the 47 pngs on the output folder, ready to use directly by optifine.
 * **Warning, the program doesn't care if it overwrites something.**
 * If the program can't find the images, it will tell you wich images it can't find, make sure that the files are named EXACTLY as it tells you(0.png, 1.png, 2.png, 3.png and 4.png). These files must comply with optifine's compact_CTM template for the program to output correctly.
