from datasets import load_dataset



if __name__ == '__main__':
    cnt =0
    dataset = load_dataset('oscar', "unshuffled_deduplicated_en", split='train', streaming=True)
    data = []
    for item in dataset:
        data.append(item)
        cnt+=1
        if cnt == 2:
            break

    print(data)


