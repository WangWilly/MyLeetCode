function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

type Tsk = {
  str: string;
  delay: number;
};

class Test {
  private que: Tsk[] = [];

  constructor() {}

  addItem(item: Tsk): Promise<void> {
    return new Promise(async (resolve) => {
      if (this.que.length !== 0) {
        console.log("added", item);
        this.que.push(item);
        resolve();
        return;
      }

      console.log("first", item);
      this.que.push(item);

      const f = async () => {
        if (this.que.length === 0) {
          return;
        }

        await sleep(this.que[0].delay);
        console.log(this.que[0].str);
        this.que.shift();

        await f();
      };

      await f();
      resolve();
    });
  }
}

const t1 = new Test();
t1.addItem({ str: "1", delay: 5000 });
t1.addItem({ str: "2", delay: 3000 });

const t2 = new Test();
Promise.all(
   [
      t2.addItem({str: "1", delay: 5000}),
      t2.addItem({str: "2", delay: 3000}),
   ]
);