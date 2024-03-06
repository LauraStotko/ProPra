import java.util.Objects;

public class MatrixKey {
    private Character structure;
    private char aa;

    public MatrixKey(Character structure, char aa) {
        this.structure = structure;
        this.aa = aa;
    }

    public char getStructure() {
        return structure;
    }

    public char getAa() {
        return aa;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        MatrixKey matrixKey = (MatrixKey) o;
        return structure == matrixKey.structure && aa == matrixKey.aa;
    }

    @Override
    public int hashCode() {
        return Objects.hash(structure, aa);
    }
}


