import java.util.*;

public class SOVScore {

    /**
     * Identifies and extracts all continuous segments of the same secondary structure type
     * from a given sequence.
     *
     * @param sequence The secondary structure sequence (actual or predicted).
     * @return A list of Segment objects representing the identified segments.
     */
    public static List<Segment> identifySegments(String sequence, char type) {
        List<Segment> segments = new ArrayList<>();
        if (sequence.isEmpty()) {
            return segments;
        }

        char currentType = sequence.charAt(0);
        int start = 0;
        for (int i = 1; i <= sequence.length(); i++) {
            if (i == sequence.length() || sequence.charAt(i) != currentType) {
                if (currentType == type) {
                    segments.add(new Segment(currentType, start, i - 1));
                }
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
    public static double calculateSOVScore(String actualStructure, String predictedStructure, char structureType) {
        return calculateSOVScore(actualStructure, predictedStructure, structureType, false)[0];
    }
    /**
     * Calculates the SOV score for a given secondary structure type.
     *
     * @param actualStructure The actual secondary structure sequence.
     * @param predictedStructure The predicted secondary structure sequence.
     * @param structureType The type of secondary structure to calculate the SOV score for ('H', 'E', or 'C').
     * @return The SOV score for the specified secondary structure type.
     */
    public static double[] calculateSOVScore(String actualStructure, String predictedStructure, char structureType,
                                           boolean shortVersion) {
        int i = 0;

        while (i< predictedStructure.length() && predictedStructure.charAt(i)=='-'){
            i++;
        }
        if(i==predictedStructure.length())
        {
            return new double[]{-1};
        }
        actualStructure=actualStructure.substring(i, actualStructure.length()-i);
        predictedStructure=predictedStructure.substring(i, predictedStructure.length()-i);
        List<Segment> actualSegments = identifySegments(actualStructure, structureType);
        List<Segment> predictedSegments = identifySegments(predictedStructure, structureType);

        double scoreSum = 0;
        int totalLen = 0;
        for (Segment actual : actualSegments) {
            boolean empty_bucket = true;
            for (Segment predicted : predictedSegments) {
                int overlap = minov(actual, predicted);
                if (overlap > 0) {
                    int maxOverlap = maxov(actual,predicted);//Math.min(actual.length(), predicted.length());
                    int delta = delta(actual, predicted);
                    scoreSum += actual.length() * ((double) overlap + delta) / maxOverlap;
                    totalLen += actual.length();
                    empty_bucket = false;
                }
            }
            if (empty_bucket) {
                totalLen += actual.length();
            }
        }

        if (totalLen <= 0){
            return new double[]{-1, totalLen};
        }

        if (shortVersion) {
            return new double[]{scoreSum, totalLen};
        } else {
            return new double[]{(scoreSum / totalLen) * 100.0};
        }
    }
}
