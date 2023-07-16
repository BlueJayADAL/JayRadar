from pipeline import DeepLearning
import multiprocessing as mp

if __name__ == '__main__':
    mp.set_start_method('spawn')

    test_pipeline = DeepLearning()

    pipeline_process = mp.Process(target=test_pipeline.run_pipeline)

    pipeline_process.start()

    input("Press Enter to stop")

    pipeline_process.terminate()

    pipeline_process.join()