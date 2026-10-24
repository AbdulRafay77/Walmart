import java.util.Collections;
import java.util.NoSuchElementException;
import java.util.PriorityQueue;
import java.util.Random;

/** Standalone verification; compile and run without Gradle or JUnit. */
public final class PowerOfTwoMaxHeapTest {
    private static void check(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }

    public static void main(String[] args) {
        boolean negativeRejected = false;
        try {
            new PowerOfTwoMaxHeap(-1);
        } catch (IllegalArgumentException expected) {
            negativeRejected = true;
        }
        check(negativeRejected, "A negative exponent must be rejected");

        int[] exponents = {0, 1, 2, 3, 5, 10, 20, 30, 31, 62, 100};
        for (int exponent : exponents) {
            PowerOfTwoMaxHeap heap = new PowerOfTwoMaxHeap(exponent);
            PriorityQueue<Integer> reference = new PriorityQueue<>(Collections.reverseOrder());
            boolean emptyRejected = false;
            try {
                heap.popMax();
            } catch (NoSuchElementException expected) {
                emptyRejected = true;
            }
            check(emptyRejected, "Empty pop must throw for exponent " + exponent);

            Random random = new Random(1000 + exponent);
            // Randomized mixed operations and duplicate/negative values.
            for (int operation = 0; operation < 2000; operation++) {
                if (reference.isEmpty() || random.nextInt(4) != 0) {
                    int value = random.nextInt(2001) - 1000;
                    heap.insert(value);
                    reference.add(value);
                } else {
                    int expected = reference.remove();
                    int actual = heap.popMax();
                    check(actual == expected,
                            "Mismatch for exponent " + exponent + " at operation " + operation);
                }
            }
            heap.insert(Integer.MIN_VALUE);
            reference.add(Integer.MIN_VALUE);
            heap.insert(Integer.MAX_VALUE);
            reference.add(Integer.MAX_VALUE);

            while (!reference.isEmpty()) {
                check(heap.popMax() == reference.remove(),
                        "Drain mismatch for exponent " + exponent);
            }
            System.out.println("PASS: childrenExponent=" + exponent);
        }
        System.out.println("All heap tests passed.");
    }
}
