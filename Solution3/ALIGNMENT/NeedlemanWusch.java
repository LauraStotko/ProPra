package Solution3.ALIGNMENT;

public class NeedlemanWusch {

    double [][] scoringMatrix;

    String pdbId1;
    String pdbId2;

    String seq2;
    String seq1;


    int gapPenalty;
    SubstitutionMatrix substitutionMatrix;

    public NeedlemanWusch(String substitutionMatrixPath, int gapPenalty){

        this.pdbId1 = "ID1";
        this.pdbId2 = "ID2";

        this.seq2 = "TATAAT";
        this.seq1 = "TTACGTAAGC";

        this.substitutionMatrix = new SubstitutionMatrix(substitutionMatrixPath);
        this.gapPenalty = gapPenalty;
        this.scoringMatrix = new double[seq1.length() + 1][seq2.length() + 1];

        initializeMatrix();
        fillMatrix();
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
                double matchOrMismatchCost = getMatchOrMismatchValue(i,j);
                double costSubstitute = scoringMatrix[i - 1][j - 1] + matchOrMismatchCost;
                double costDelete = scoringMatrix[i - 1][j] + gapPenalty;
                double costInsert = scoringMatrix[i][j - 1] + gapPenalty;
                scoringMatrix[i][j] = Math.max(Math.max(costDelete, costInsert), costSubstitute);
            }
        }
    }

    public AlignmentResult backtrack() {
        StringBuilder alignmentSeq1 = new StringBuilder();
        StringBuilder alignmentSeq2 = new StringBuilder();

        int i = seq1.length();
        int j = seq2.length();

        // Backtracking loop
        while (i > 0 || j > 0) {
            // Error Handling for index out of bounds with Integer.MIN_VALUE
            double currentScore = i > 0 && j > 0 ? scoringMatrix[i][j] : Integer.MIN_VALUE;
            double scoreDiagonal = i > 0 && j > 0 ? scoringMatrix[i - 1][j - 1] : Integer.MIN_VALUE;
            double scoreUp = i > 0 ? scoringMatrix[i - 1][j] : Integer.MIN_VALUE;
            double scoreLeft = j > 0 ? scoringMatrix[i][j - 1] : Integer.MIN_VALUE;
            double matchOrMismatchValue = (i > 0 && j > 0) ? getMatchOrMismatchValue(i, j) : Integer.MIN_VALUE;

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

        double alignmentScore = scoringMatrix[seq1.length()][seq2.length()];

        AlignmentResult alignmentResult = new AlignmentResult(this.pdbId1, this.pdbId2, alignmentScore, alignmentSeq1.toString(), alignmentSeq2.toString());

        return alignmentResult;
    }

    private double getMatchOrMismatchValue(int i, int j) {
        char a = seq1.charAt(i - 1);
        char b = seq2.charAt(j - 1);
        return substitutionMatrix.getScore(a, b);
    }

    public void printMatrix() {
        fillMatrix();
        // Define the width for each column. Adjust the value as needed.
        int columnWidth = 7;

        // Print the top row (seq2 characters)
        System.out.print(String.format("%" + (columnWidth * 2) + "s", "")); // Padding for alignment
        for (int j = 0; j < seq2.length(); j++) {
            System.out.print(String.format("%-" + columnWidth + "s", seq2.charAt(j)));
        }
        System.out.println(); // Newline after printing seq2 characters

        for (int i = 0; i <= seq1.length(); i++) {
            if (i > 0) { // Print seq1 character at the start of each row, excluding the first row
                System.out.print(String.format("%-" + columnWidth + "s", seq1.charAt(i - 1)));
            } else {
                System.out.print(String.format("%-" + columnWidth + "s", " ")); // Padding for the first row
            }
            for (int j = 0; j <= seq2.length(); j++) {
                // Format the score with fixed width for alignment, adjust precision as needed
                System.out.print(String.format("%-" + columnWidth + ".2f", scoringMatrix[i][j])); // Print each cell's value
            }
            System.out.println(); // Newline at the end of each row
        }
    }

}
