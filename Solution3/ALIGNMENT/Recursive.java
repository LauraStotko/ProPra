package Solution3.ALIGNMENT;

import java.util.List;
import java.util.Map;

public class Recursive {
    int match;
    int mismatch;
    int gapPenalty;

    Map<String, String> sequences;
    List<PdbPair> alignments;

    public Recursive(int match, int mismatch, int gapOpenValue, Map<String, String> sequences, List<PdbPair> alignments) {
        this.match = match;
        this.mismatch = mismatch;
        this.gapPenalty = gapOpenValue;
        this.alignments = alignments;
        this.sequences = sequences;
    }

    public void calculateAlignment() {
        for (PdbPair pair : alignments) {
            String seq1 = sequences.get(pair.getPdbId1());
            String seq2 = sequences.get(pair.getPdbId2());

            if (seq1 != null && !seq1.isEmpty() && seq2 != null && !seq2.isEmpty()) {
                int score = calculateAlignmentScore(seq1, seq2, seq1.length(), seq2.length());

                System.out.println("For PDB IDs " + pair.getPdbId1() + " and "
                        + pair.getPdbId2() + ", the alignment score is: " + score);
            } else {
                System.out.println("One or both sequences for PDB IDs " + pair.getPdbId1()
                        + " and " + pair.getPdbId2() + " are missing or empty.");
            }
        }
    }


    private int calculateAlignmentScore(String seq1, String seq2, int i, int j) {
        // Base cases (Termination Condition)
        if (i == 0) return j * gapPenalty; // Penalize remaining length of seq2
        if (j == 0) return i * gapPenalty; // Penalize remaining length of seq1

        // RECURSIVE CASES
        // Determine if the current characters match or mismatch
        int matchOrMismatchCost = (seq1.charAt(i - 1) == seq2.charAt(j - 1)) ? match : mismatch;
        // Calculate cost for matching or mismatching the last characters
        int costSubstitute = calculateAlignmentScore(seq1, seq2, i - 1, j - 1) + matchOrMismatchCost;
        // Calculate cost for deleting a character from seq1 (adding a gap in seq2)
        int costDelete = calculateAlignmentScore(seq1, seq2, i - 1, j) + gapPenalty;
        // Calculate cost for inserting a character into seq1 (adding a gap in seq1)
        int costInsert = calculateAlignmentScore(seq1, seq2, i, j - 1) + gapPenalty;

        // Return the maximum cost among delete, insert, and substitute
        return Math.max(Math.max(costDelete, costInsert), costSubstitute);
    }
}

