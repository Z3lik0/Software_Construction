import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public abstract class Archive {
    protected Path sourceDir;
    protected FileHasher fileHasher;

    public Archive(String sourceDir) {
        this.sourceDir = Paths.get(sourceDir);
        this.fileHasher = new FileHasher();
    }

    public List<FileEntry> backup() {
        List<FileEntry> manifest = fileHasher.hashAll(sourceDir);
        writeManifest(manifest);
        copyFiles(manifest);
        return manifest;
    }

    abstract protected void writeManifest(List<FileEntry> manifest);

    abstract protected void copyFiles(List<FileEntry> manifest);
}