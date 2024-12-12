/**
 * @file random_binary_sequence.cpp
 * @brief Generating a random sequence of binary numbers.
 */

#include <iostream>
#include <cstdlib>
#include <ctime>
#include <sstream>

using namespace std;

/**
 * @brief Generates a random sequence of binary numbers of a given size.
 * @param size The size of the sequence.
 * @return A string representing the random sequence of binary numbers.
 */
string generateRandomBinarySequence(int size) {
    string binarySequence = "";
    for (int i = 0; i < size; ++i) {
        int randomBit = rand() % 2; // Генерация случайного бита (0 или 1)
        stringstream ss;
        ss << randomBit;
        binarySequence += ss.str(); // Добавление бита к последовательности
    }
    return binarySequence;
}

/**
 * @brief The main function.
 * @return 0 on successful completion.
 */
int main() {
    srand(time(0));

    int size;
    cout << "Введите размер последовательности бинарных чисел: ";
    cin >> size;

    string binarySequence = generateRandomBinarySequence(size);

    cout << "Случайная последовательность бинарных чисел размером " << size << ":\n";
    cout << binarySequence << endl;

    return 0;
}
