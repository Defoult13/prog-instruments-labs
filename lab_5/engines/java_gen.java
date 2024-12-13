import java.util.Random;

/**
 * This class generates a random binary sequence of a specified size.
 */
public class RandomBinaryGenerator {

    /**
     * Main method to generate and print a random binary sequence.
     * @param args Command-line arguments (not used)
     */
    public static void main(String[] args) {
        int size = 10;
        String randomBinarySequence = generateRandomBinarySequence(size);
        System.out.println("Random binary sequence: " + randomBinarySequence);
    }

    /**
     * Generates a random binary sequence of the specified size.
     * @param size The size of the binary sequence to generate
     * @return The random binary sequence as a string
     */
    public static String generateRandomBinarySequence(int size) {
        Random random = new Random();
        StringBuilder binarySequence = new StringBuilder();

        for (int i = 0; i < size; i++) {
            int randomBit = random.nextInt(2);
            binarySequence.append(randomBit);
        }
        return binarySequence.toString();
    }
}
