package Solution3.ALIGNMENT;

import java.util.List;
import java.util.Map;

public class OutputHandler {
    private String pdbId1;
    private String pdbId2;
    private double alignmentScore;
    private String alignmentSeq1;
    private String alignmentSeq2;
    private String outputFormat;
    private String dpMatricesDir; // Directory to save dynamic programming matrices, if specified

    public OutputHandler(AlignmentResult alignmentResult, String outputFormat, String dpMatricesDir) {
        this.pdbId1 = alignmentResult.getPdbId1();
        this.pdbId2 = alignmentResult.getPdbId2();
        this.alignmentScore = alignmentResult.getAlignmentScore();
        this.alignmentSeq1 = alignmentResult.getAlignmentSeq1();
        this.alignmentSeq2 = alignmentResult.getAlignmentSeq2();
        this.outputFormat = outputFormat;
        this.dpMatricesDir = dpMatricesDir;
    }

    public OutputHandler(AlignmentResult alignmentResult, String outputFormat) {
        this.pdbId1 = alignmentResult.getPdbId1();
        this.pdbId2 = alignmentResult.getPdbId2();
        this.alignmentScore = alignmentResult.getAlignmentScore();
        this.alignmentSeq1 = alignmentResult.getAlignmentSeq1();
        this.alignmentSeq2 = alignmentResult.getAlignmentSeq2();
        this.outputFormat = outputFormat;
    }



    /**
     * Handles the output based on the specified format.
     */
    public void handleOutput() {
        switch (outputFormat) {
            case "scores":
                printScores();
                break;
            case "ali":
                printAlignments();
                break;
            case "html":
                printHtmlOutput();
                break;
            default:
                System.err.println("Invalid output format specified.");
                break;
        }

        if (dpMatricesDir != null && !dpMatricesDir.isEmpty()) {
            writeDpMatrices();
        }
    }

    private void printScores() {
        // Iterate over alignments and print scores
        // Example: System.out.println(pdbId1 + " " + pdbId2 + " " + score);
        System.out.println(pdbId1 + " " + pdbId2 + " " + alignmentScore);
    }

    private void printAlignments() {
        // Perform alignments and print in 'ali' format
        // Example:
        // >pdbId1 pdbId2 score
        // pdbId1: sequence1
        // pdbId2: sequence2
        System.out.println(">" + pdbId1 + " " + pdbId2 + " " + alignmentScore);
        System.out.println(pdbId1 + ": " + alignmentSeq1);
        System.out.println(pdbId2 + ": " + alignmentSeq2);
    }

    private void printHtmlOutput() {
        // Generate and print HTML output including additional information and formatted alignments
    }

    private void writeDpMatrices() {
        // Depending on the format ('ali', 'html'), write the DP matrices to files in the specified directory
        // For 'html' format, highlight the backtracking path of the computed optimal alignment
    }

    // Additional methods to perform alignments, calculate scores, and manage file I/O operations
}

