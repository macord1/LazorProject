# LazorProject

This is a group project for Software Carpentry EN.540.635 to find solutions to the Lazors game on android and iPhone.
Group members and their emails:
  Molly Acord, macord1@jhu.edu
  Sreelakshmi Sunil, ssunil1@jhu.edu

Files included in final release v.final : Lazor.py, unit_tests.py, dark_1.bff, mad_1.bff, mad_4.bff, mad_7.bff, numbered_6.bff, showstopper_4.bff, tiny_5.bff, and yarn_5.bff

Lazor.py is the master code for this project. Unit_tests.py is used to make sure the different functions in the master code are returning what is expected.

Method of solving: After a board is read in, the lazor path(s) is/are calculated. All block layout combinations will be collected and tested until the lazor path(s) reach the desired point(s). 

You can change the board you wish to solve by putting its file name in the main function in Lazor.py
The final solution will appear in a text file called solution.txt

There is another branch in this repository called updates. This is where we added code developments along the way, but they are not needed for to solve the games.
