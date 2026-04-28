from pdf_core.graph.pipeline import run_graph_pipeline


def main() -> None:
    print("Building graph from chunk artifacts...")
    run_graph_pipeline()


if __name__ == "__main__":
    main()
