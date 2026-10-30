# How to Learn to Build a Basic Clock in LogicSim
### Written by 12zcab

Yay lets pickup from where we left last time and continue our journey!!!

So in the last chapter, we have successfully built a Seven Segment Counter

![SevenSegmentCounter](IMG/SevenSegmentCounter.gif)

And this time, we are going to build a Seven Segment Based Clock.

## Targeted Features for the product

- Accuracy (we need it to really count real time)
- 4 Digit Decimal Output with seven segment(Minute,Second)
- Configurable Time Data

## We feature we need to make the counter to become a real clock?

- we need a sexagesimal counter
- we need a Register that have Write ability and also have Increasement and Reset Ability

## Complex Register with Increasement,Reset and Rewrite function.

### JK FlipFlop

### Clock and Reset 

    Common control signal

### Toggling with JK FlipFlop

    (T is actually just JK when they are same)
    So when Increasement mode we can just directly put the previous output as the new input's JK signal

### Force Rewrite a JK FlipFlop

    lol just D->J and !D->K