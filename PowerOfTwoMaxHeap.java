import java.util.Arrays;
import java.util.NoSuchElementException;

/**
 * An array-backed max heap with 2^childrenExponent children per internal node.
 * Supports negative values and duplicates. Does not use boxed Integers.
 */
public final class PowerOfTwoMaxHeap {
    private final int branchingFactor;
    private int[] elements;
    private int size;

    /**
     * @param childrenExponent nonnegative exponent defining the branching factor
     */
    public PowerOfTwoMaxHeap(int childrenExponent) {
        if (childrenExponent < 0) {
            throw new IllegalArgumentException("childrenExponent must be nonnegative");
        }
        // An int[] cannot hold 2^31 elements. Cap the effective branching
        // factor so large exponents do not overflow a Java int.
        this.branchingFactor = childrenExponent >= 31
                ? Integer.MAX_VALUE
                : 1 << childrenExponent;
        this.elements = new int[16];
        this.size = 0;
    }

    /** Inserts a value, restoring the max-heap property by sifting upward. */
    public void insert(int value) {
        if (size == elements.length) {
            int capacity = elements.length;
            int newCapacity = capacity < (Integer.MAX_VALUE - 8) / 2
                    ? capacity * 2
                    : Integer.MAX_VALUE - 8;
            if (newCapacity <= capacity) {
                throw new IllegalStateException("Heap capacity exceeded");
            }
            elements = Arrays.copyOf(elements, newCapacity);
        }

        int index = size++;
        while (index > 0) {
            int parentIndex = (index - 1) / branchingFactor;
            if (elements[parentIndex] >= value) {
                break;
            }
            elements[index] = elements[parentIndex];
            index = parentIndex;
        }
        elements[index] = value;
    }

    /** Removes and returns the largest value. */
    public int popMax() {
        if (size == 0) {
            throw new NoSuchElementException("Cannot pop from an empty heap");
        }

        int maximum = elements[0];
        int lastValue = elements[--size];
        if (size == 0) {
            return maximum;
        }

        int index = 0;
        // The final possible parent is floor((size - 2) / branchingFactor).
        while (index <= (size - 2) / branchingFactor) {
            int firstChild = index * branchingFactor + 1;
            int childLimit = (int) Math.min((long) size,
                    (long) firstChild + branchingFactor);

            int largestChild = firstChild;
            for (int child = firstChild + 1; child < childLimit; child++) {
                if (elements[child] > elements[largestChild]) {
                    largestChild = child;
                }
            }
            if (elements[largestChild] <= lastValue) {
                break;
            }
            elements[index] = elements[largestChild];
            index = largestChild;
        }
        elements[index] = lastValue;
        return maximum;
    }
}
