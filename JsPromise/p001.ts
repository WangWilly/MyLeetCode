function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

type Tsk = {
  func: () => Promise<string>;
  delay: number;
};

class Test {
  private que: Tsk[] = [];

  constructor() {}

  addItem(item: Tsk): Promise<Tsk> {
    return new Promise(async (resolve) => {
      if (this.que.length !== 0) {
        this.que.push(item);
        resolve(item);
        return;
      }

      this.que.push(item);

      while (this.que.length !== 0) {
        await sleep(this.que[0].delay);
        try {
          const s = await this.que[0].func();
          console.log(s);
        } catch (err) {
          console.log("err catched");
          console.log(err);
        }

        this.que.shift();
      }

      resolve(item);
    });
  }
}

const t = new Test();
Promise.all([
  t.addItem({
    func: () => new Promise((resolve) => resolve("1")),
    delay: 5000,
  }),
  t.addItem({
    func: () => new Promise((resolve, reject) => reject("2")),
    delay: 3000,
  }),
]);
