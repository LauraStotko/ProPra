package Solution3.ALIGNMENT;

import java.util.List;
import java.util.Map;

public class OutputHandler {
    private List<PdbPair> alignments;
    private Map<String, String> sequences;
    private String outputFormat;
    private String dpMatricesDir; // Directory to save dynamic programming matrices, if specified

    public OutputHandler(List<PdbPair> alignments, Map<String, String> sequences, String outputFormat, String dpMatricesDir) {
        this.alignments = alignments;
        this.sequences = sequences;
        this.outputFormat = outputFormat;
        this.dpMatricesDir = dpMatricesDir;
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
    }

    private void printAlignments() {
        // Perform alignments and print in 'ali' format
        // Example:
        // >pdbId1 pdbId2 score
        // pdbId1: sequence1
        // pdbId2: sequence2
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

