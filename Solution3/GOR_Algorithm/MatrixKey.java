import java.util.Objects;

public class MatrixKey {
    //private Character structure;
    private char aa;

    private int index_window;
    private Character aa_subwindow;

    public MatrixKey(Character aa_subwindow, char aa, int index_window) {
        //this.structure = structure;
        this.aa = aa;
        this.index_window = index_window;
        this.aa_subwindow = aa_subwindow;
    }

    public char getAa() {
        return aa;
    }

    public char getAa_subwindow() {
        return aa_subwindow;
    }

    public int getIndex_window() {
        return index_window;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        MatrixKey matrixKey = (MatrixKey) o;
        return aa == matrixKey.aa && aa_subwindow == matrixKey.aa_subwindow && index_window == matrixKey.index_window;
    }

    @Override
    public int hashCode() {
        return Objects.hash(aa, aa_subwindow, index_window);
    }
}
