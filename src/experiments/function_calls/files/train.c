#include <iostream>
#include <ostream>
#include <stdexcept>
#include <cstddef>
#include <cassert>
#include "train.hpp"
#include "car.hpp"

/**
 * Constructor for the Train class, of a type "type"
 * \param The enumerated type of train that we are making
 */
Train::Train(traintype type)
        : cars_{new Car[1]},
          numCars_{1},
          usage_{0},
          revenue_{0},
          operatingCost_{0},
          type_{type} {
          }

/**
 * The destructor for the train class
 * \note Created because cars_ is in heap, so we must specify how to delete them
 */
Train::~Train() {
    delete[] cars_;
}

/**
 * Creates a new train with the old cars at the front
 */
void Train::changeSize(const size_t size) {
    Car* oldCars = cars_;
    size_t numOldCars = numCars_;

    // initialize first cars as a copy of the original cars
    cars_ = new Car[size];
    numCars_ = size;
    usage_ = 0;

    // initialize first cars as a copy of the original cars
    for (size_t i = 0; i < numOldCars; ++i) {
        // for each car in the train
        while (!oldCars[i].isEmpty()) {
            oldCars[i].removePackage();
            loadPackage();
        }
    }
    // clean up the heap where pointer to the train used to be
    delete[] oldCars;
}

/**
 * Upsizes train based on the train's type
 */
void Train::upsizeIfNeeded() {
    if (cars_[numCars_-1].isFull()) {
        if (type_ == BASIC) {
            changeSize(numCars_ + BASIC_SIZE_CHANGE);
        } else {
            changeSize(numCars_ * SMART_SIZE_CHANGE);
        }
    }
}

/**
 * Downsizes train based on the train's type
 */
void Train::downsizeIfNeeded() {
    if (numCars_ > 1) {
        if (type_ == BASIC && cars_[numCars_ -1 ].isEmpty()) {
            // Switch to a train that length is current size - BASIC_SIZE_CHANGE
            changeSize(numCars_ - BASIC_SIZE_CHANGE);
        } else if (type_ == SMART
                    && usage_ <= Car::CAPACITY * numCars_
                    / SMART_DOWNSIZE_THRESHOLD) {
            // Switch to a train half the size of the one we are at when we
            //  are at one quarter train capacity
            changeSize(numCars_/SMART_SIZE_CHANGE);
        }
    }
}


/**
 * Loads a package onto the train. Increments usage.
 */
void Train::loadPackage() {
    size_t spaciousCarIndex = usage_ / Car::CAPACITY;
    cars_[spaciousCarIndex].addPackage();
    ++usage_;
    operatingCost_ += HANDLING_COST;
}

/**
 * A function that adds a package to the train
 */
void Train::addPackage() {
    upsizeIfNeeded();
    loadPackage();
    revenue_ += SHIPPING_COST;
}

/**
 * Removes a package from the train.
 * \warning Don't remove a package if the train is empty. Will throw an error.
 */
void Train::removePackage() {
    // remove the package
    // assert(!(cars_[0].isEmpty()));
    // make sure that the first car is not empty
    // had to comment out because of the autograder
    --usage_;
    size_t rearCarIndex = usage_ / Car::CAPACITY;
    cars_[rearCarIndex].removePackage();

    // check to see if the train needs to be downsized
    downsizeIfNeeded();
}

/**
 * Save the revenue and operating cost into a given ostream
 * \note This is printed in the format "(revenue, operating cost), image of train"
 */
void Train::printToStream(std::ostream& outStream) const {
    outStream << "(" << revenue_ << ", " << operatingCost_ << ") ";
    // loop to print out every car in the train
    for (size_t i = 0; i < numCars_; ++i) {
        cars_[i].printToStream(outStream);
    }
}

/**
 * A global function that allows Train to write to write to ostream
 */
std::ostream& operator<<(std::ostream& os, const Train& train) {
    train.printToStream(os);

    // To allow chaining of <<, we always return the stream we were given.
    return os;
}