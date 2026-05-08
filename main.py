import sys
from pathlib import Path

src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PyQt6.QtWidgets import QApplication, QMessageBox
from ui.main_window import MainWindow
from pipeline.controller import PipelineController

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    controller = PipelineController()

    def on_recognize_requested():
        pixels = window.left_panel.canvas.export_pixels()
        try:
            state = controller.run(pixels)
        except Exception as exc:
            window.right_panel.update_prediction(f"Error: {exc}", None, None)
            return
        window.right_panel.update_prediction(
            state.prediction, state.confidence, state.runner_up
        )
        window.right_panel.update_visualizations(state)

    window.recognize_requested.connect(on_recognize_requested)

    def on_save_sample_requested(label: str):
        pixels = window.left_panel.canvas.export_pixels()
        ok = controller.save_sample(label, pixels)
        if ok:
            counts = controller.training_manager.get_class_counts()
            _update_library_list(counts)
        else:
            QMessageBox.warning(
                window,
                "Save Sample Failed",
                "Could not save sample.\n"
                "Make sure:\n"
                "  • You have drawn something on the canvas\n"
                f"  • The label is not empty and ≤ 10 characters (got: '{label}')",
            )

    def _update_library_list(counts: dict):
        lst = window.left_panel._lst_templates
        lst.clear()
        for lbl in sorted(counts.keys()):
            lst.addItem(f"{lbl}  ({counts[lbl]})")

    window.save_sample_requested.connect(on_save_sample_requested)

    def on_clear_requested():
        window.right_panel.clear_results()
        window.right_panel.clear_visualizations()

    window.clear_requested.connect(on_clear_requested)

    counts = controller.training_manager.get_class_counts()
    if counts:
        _update_library_list(counts)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
