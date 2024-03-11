import java.util.*;
import java.util.stream.Collectors;

public class SOVScore {

    /**
     * Identifies and extracts all continuous segments of the same secondary structure type
     * from a given sequence.
     *
     * @param sequence The secondary structure sequence (actual or predicted).
     * @return A list of Segment objects representing the identified segments.
     */
    private static List<Segment> identifySegments(String sequence) {
        List<Segment> segments = new ArrayList<>();
        if (sequence.isEmpty()) {
            return segments;
        }

        char currentType = sequence.charAt(0);
        int start = 0;
        for (int i = 1; i <= sequence.length(); i++) {
            if (i == sequence.length() || sequence.charAt(i) != currentType) {
                segments.add(new Segment(currentType, start, i - 1));
                if (i < sequence.length()) {
                    currentType = sequence.charAt(i);
                    start = i;
                }
            }
        }
        return segments;
    }

    /**
     * Calculates the minimum overlap between two segments.
     *
     * @param s1 The first segment.
     * @param s2 The second segment.
     * @return The minimum overlap length between the two segments.
     */
    public static int minov (Segment s1, Segment s2){
        int overlapStart = Math.max(s1.getStart(), s2.getStart());
        int overlapEnd = Math.min(s1.getEnd(), s2.getEnd());

        if (overlapStart <= overlapEnd) {
            return overlapEnd - overlapStart + 1;
        } else {
            return 0; // No overlap
        }
    }

    /**
     * Calculates the maximum possible overlap between two segments.
     *
     * @param s1 The first segment.
     * @param s2 The second segment.
     * @return The maximum overlap length, considering potential adjustments.
     */
    public static int maxov (Segment s1, Segment s2){
        if (minov(s1, s2) == 0) {
            return 0; // No initial overlap, might need to adjust based on your SOV requirements
        }

        // The maximum overlap is the length of the shorter segment
        //return Math.min(s1.length(), s2.length());

        int overlapStart = Math.min(s1.getStart(), s2.getStart());
        int overlapEnd = Math.max(s1.getEnd(), s2.getEnd());

        return overlapEnd - overlapStart + 1;
    }

    /**
     * Calculates the delta value used in SOV score calculation, providing a bonus for partial overlaps.
     *
     * @param s1 The first segment (actual segment).
     * @param s2 The second segment (predicted segment).
     * @return The delta value considering the overlaps and lengths of the segments.
     */
    public static int delta(Segment s1, Segment s2) {
        int minOverlap = minov(s1, s2);
        int maxOverlap = maxov(s1, s2);

        if (minOverlap == 0) {
            return 0; // No overlap means no delta
        }

        // Calculating the components of the delta formula
        int overlapDifference = maxOverlap - minOverlap;
        int halfLengthS1 = s1.length() / 2; // int durch int rundet ab
        int halfLengthS2 = s2.length() / 2;

        // Delta is the minimum of these values
        return Math.min(overlapDifference, Math.min(minOverlap, Math.min(halfLengthS1, halfLengthS2)));
    }

    // Step 3: SOV Score Calculation
    /**
     * Calculates the SOV score for a given secondary structure type.
     *
     * @param actualStructure The actual secondary structure sequence.
     * @param predictedStructure The predicted secondary structure sequence.
     * @param structureType The type of secondary structure to calculate the SOV score for ('H', 'E', or 'C').
     * @return The SOV score for the specified secondary structure type.
     */
    public static double calculateSOVScore(String actualStructure, String predictedStructure, char structureType) {
        String oldA = actualStructure;
        String oldP = predictedStructure;
        actualStructure = actualStructure.substring(8,actualStructure.length()-8);
        predictedStructure = predictedStructure.substring(8,predictedStructure.length()-8);
        List<Segment> actualSegments = identifySegments(actualStructure);
        List<Segment> predictedSegments = identifySegments(predictedStructure);

        actualSegments = filterSegmentsByType(actualSegments, structureType);
        predictedSegments = filterSegmentsByType(predictedSegments, structureType);

        double scoreSum = 0;
        int totalLen = 0;
        for (Segment actual : actualSegments) {
            boolean empty_bucket = true;
            for (Segment predicted : predictedSegments) {
                int overlap = actual.calculateOverlap(predicted);
                if (overlap > 0) {
                    int maxOverlap = Math.min(actual.length(), predicted.length());
                    int delta = delta(actual,predicted);
                    scoreSum += ((double) overlap + delta) / maxOverlap * actual.length();
                    totalLen += actual.length();
                    empty_bucket = false;
                }
            }
            if (empty_bucket){
                totalLen += actual.length();
            }
        }

        double result = totalLen > 0 ? (scoreSum / totalLen) * 100.0 : 0.0;
        return result;
    }


    private static List<Segment> filterSegmentsByType(List<Segment> segments, char type) {
        return segments.stream().filter(segment -> segment.getType() == type).collect(Collectors.toList());
    }

}
