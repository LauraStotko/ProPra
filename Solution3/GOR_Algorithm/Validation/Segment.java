public class Segment {
    private char type; // Typ des Segments ('H', 'E', 'C')
    private int start; // Startindex des Segments in der Sequenz
    private int end;   // Endindex des Segments in der Sequenz

    /**
     * Konstruktor für ein Segment.
     *
     * @param type  Der Typ des Segments (z.B. 'H', 'E', 'C').
     * @param start Der Startindex des Segments in der Sequenz.
     * @param end   Der Endindex des Segments in der Sequenz.
     * @throws IllegalArgumentException wenn der Startindex größer als der Endindex ist.
     */
    public Segment(char type, int start, int end) {
        if (start > end) {
            throw new IllegalArgumentException("Startindex darf nicht größer als Endindex sein.");
        }
        this.type = type;
        this.start = start;
        this.end = end;
    }

    // Getter-Methoden
    public char getType() {
        return type;
    }

    public int getStart() {
        return start;
    }

    public int getEnd() {
        return end;
    }

    /**
     * Berechnet die Länge des Segments.
     *
     * @return Die Länge des Segments.
     */
    public int length() {
        return end - start + 1;
    }

    /**
     * Berechnet die Überlappung zwischen diesem Segment und einem anderen.
     *
     * @param other Das andere Segment.
     * @return Die Länge der Überlappung.
     */
    public int calculateOverlap(Segment other) {
        if (this.end < other.start || other.end < this.start) {
            // Keine Überlappung.
            return 0;
        }
        // Berechnung der Überlappungslänge.
        int overlapStart = Math.max(this.start, other.start);
        int overlapEnd = Math.min(this.end, other.end);
        return overlapEnd - overlapStart + 1;
    }

    /**
     * Prüft, ob dieses Segment mit einem anderen Segment überlappt.
     *
     * @param other Das andere Segment.
     * @return true, wenn eine Überlappung besteht, sonst false.
     */
    public boolean overlapsWith(Segment other) {
        return this.start <= other.end && this.end >= other.start;
    }

    /**
     * Gibt eine String-Repräsentation des Segments zurück.
     *
     * @return Eine String-Repräsentation des Segments.
     */
    @Override
    public String toString() {
        return String.format("Segment{type=%c, start=%d, end=%d, length=%d}", type, start, end, length());
    }
}
