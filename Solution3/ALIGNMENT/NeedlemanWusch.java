package Solution3.ALIGNMENT;

import java.util.List;
import java.util.Map;

public class NeedlemanWusch extends SequenceAlignment {
    int [][] scoringMatrix;
    Map<String, String> sequences;
    private List<PdbPair> alignments;
    String seq2 = "TATAAT";
    String seq1 = "TTACGTAAGC";

    int gapPenalty = -4;

    int match = 3;
    int mismatch = -2;

    public NeedlemanWusch(){
        this.scoringMatrix = new int[seq1.length() + 1][seq2.length() + 1];
        initializeMatrix();
    }

    public void initializeMatrix(){
        // Goes through each row
        for (int i = 0; i <= seq1.length(); i++) {
            scoringMatrix[i][0] = i * gapPenalty;
        }
        // Goes through each column
        for (int j = 0; j <= seq2.length(); j++) {
            scoringMatrix[0][j] = j * gapPenalty;
        }
    }

    public void fillMatrix() {
        for (int i = 1; i <= seq1.length(); i++) {
            for (int j = 1; j <= seq2.length(); j++) {
                int matchOrMismatchCost = (seq1.charAt(i - 1) == seq2.charAt(j - 1)) ? match : mismatch;
                int costSubstitute = scoringMatrix[i - 1][j - 1] + matchOrMismatchCost;
                int costDelete = scoringMatrix[i - 1][j] + gapPenalty;
                int costInsert = scoringMatrix[i][j - 1] + gapPenalty;
                scoringMatrix[i][j] = Math.max(Math.max(costDelete, costInsert), costSubstitute);
            }
        }
    }

    public void backtrack() {
        StringBuilder alignmentSeq1 = new StringBuilder();
        StringBuilder alignmentSeq2 = new StringBuilder();

        int i = seq1.length();
        int j = seq2.length();

        // Backtracking loop
        while (i > 0 || j > 0) {
            // Error Handling for index out of bounds with Integer.MIN_VALUE
            int currentScore = i > 0 && j > 0 ? scoringMatrix[i][j] : Integer.MIN_VALUE;
            int scoreDiagonal = i > 0 && j > 0 ? scoringMatrix[i - 1][j - 1] : Integer.MIN_VALUE;
            int scoreUp = i > 0 ? scoringMatrix[i - 1][j] : Integer.MIN_VALUE;
            int scoreLeft = j > 0 ? scoringMatrix[i][j - 1] : Integer.MIN_VALUE;
            int matchOrMismatchValue = i > 0 && j > 0 ? getMatchOrMismatchValue(i, j) : Integer.MIN_VALUE;

            // Decide the best move
            if (i > 0 && j > 0 && currentScore == scoreDiagonal + matchOrMismatchValue) {
                alignmentSeq1.insert(0, seq1.charAt(--i)); // Diagonal move
                alignmentSeq2.insert(0, seq2.charAt(--j));
            } else if (i > 0 && (j == 0 || currentScore == scoreUp + gapPenalty)) {
                alignmentSeq1.insert(0, seq1.charAt(--i)); // Up move
                alignmentSeq2.insert(0, '-');
            } else if (j > 0 && (i == 0 || currentScore == scoreLeft + gapPenalty)) {
                alignmentSeq1.insert(0, '-'); // Left move
                alignmentSeq2.insert(0, seq2.charAt(--j));
            }
        }

        // Print the final alignment
        System.out.println("Alignment Seq1: " + alignmentSeq1);
        System.out.println("Alignment Seq2: " + alignmentSeq2);
    }

    private int getMatchOrMismatchValue(int i, int j){
        if(seq1.charAt(i - 1) == seq2.charAt(j - 1)){
            return match;
        }
        return mismatch;
    }

    public void printMatrix() {
        fillMatrix();
        // Print the top row (seq2 characters)
        System.out.print(" \t \t"); // Padding for alignment
        for (int j = 0; j < seq2.length(); j++) {
            System.out.print(seq2.charAt(j) + "\t");
        }
        System.out.println(); // Newline after printing seq2 characters

        for (int i = 0; i <= seq1.length(); i++) {
            if (i > 0) { // Print seq1 character at the start of each row, excluding the first row
                System.out.print(seq1.charAt(i - 1) + "\t");
            } else {
                System.out.print(" \t"); // Padding for the first row
            }
            for (int j = 0; j <= seq2.length(); j++) {
                System.out.print(scoringMatrix[i][j] + "\t"); // Print each cell's value
            }
            System.out.println(); // Newline at the end of each row
        }
    }
}
