# Chapter 9. The `multiprocessing` Module

## Questions You'll Be Able to Answer After This Chapter

- What does the `multiprocessing` module offer?
  `multiprocessing` 모듈은 뭘 제공하는가?

- What's the difference between processes and threads?
  Process와 Thread의 차이점?

- How do I choose the right size for a process pool?
  어떻게 적당한 크기의 Process Pool을 만들 수 있을까?

- How do I use non-persistent queues for work processing?
  영속적이지 않은 Queue들로 작업하기 (아마도 .. Job Queue에 대한 이야기)

- What are the costs and benefits of interprocess communication?
  Interprocess communication의 장단점

- How can I process `numpy` data with many CPUs?
  의) 어떻게 멀티코어로 numpy를 사용하는가?

- Why do I need locking to avoid data loss?
  왜 Data loss를 방지하기 위해 locking이 필요한가?


#### CPython은 default로 multicore를 사용하지 않는다. (python이니까..)


#### n-times speedup with n-cores.
일반적으로 코어를 많이 사용할 수록 성능은 올라간다.

#### Amdahl's Law [Wikipedia](https://en.wikipedia.org/wiki/Amdahl%27s_law)

> 암달의 법칙(Amdahl's law)은 암달의 저주로도 불리며 컴퓨터 시스템의 일부를 개선할 때 전체적으로 얼마만큼의 최대 성능 향상이 있는지 계산하는 데 사용된다. 진 암달의 이름에서 따왔다.

병렬 컴퓨팅에서 멀티 프로세서를 사용할 때 프로그램의 성능향상은 프로그램의 순차적인 부분에 의해 제한된다.
예를 들면, 프로그램의 95%가 병렬화 할 수 있다면 이론적인 최대 성능 향상은 아무리 많은 프로세서를 사용하더라도 최대 20배로 제한된다.


#### Multiprocessing module은 process, thread기반의 병렬 프로세싱을 할 수 있게 해준다.
- single-machine multicore parallelism.


#### 일반적으로 CPU-bound 문제를 병렬화 하는데 사용함.
- I/O-bound 문제에도 사용하기도 함.. (Chapter 8에서 본 `gevent`와 `tornado`, `asyncIO` 등..)
- 기존 작업을 Parallelize하기 위해선 생각할 것이 많다.
- debugging이 힘듦.
- 개발속도 저하.


#### Sharing of state in a parallel system
- parallelism에서 봉착하는 대표적인 문제 중 하나
- 큰 오버헤드가 발생할 수 있음. (오히려 역효과)
- Synchronization cost를 줄이는 방법.
- Avoiding shared state will make  your life far easier.


#### Typical Jobs for the Multiprocessing Module
- Parallelize a CPU-bound task with `Process` of `Pool` objects.
- Parallelize an I/O-bound task in a Pool with threads using the (oddly named) `dummy` module.
- Share `pickled` work via a Queue.
- Share state between parallelized workers, including bytes, primitive datatypes, dictionaries, and lists.
- An Overview of the Multiprocessing Module


## An Overview of the Multiprocessing Module

### `multiprocessing`모듈의 메인 컴포넌트들

#### `Process`
- A forked copy of the current process

#### `Pool`
- Wraps the `Process` or `threading`

#### `Queue`
- A FIFO queue allowing multiple producers and consumers.

#### `Pipe`
- A uni- or bidirectionanl communication channel between two processes.

#### `Manager`
- A high-level managed interface to share Python objects between processes.

#### `ctypes`
- Allows sharing of primitive datatypes (e.g., integers, floats, and bytes) between processes after they have forked.


#### 책에 소개된 몇가지 예제들

[몬테카를로 기법](https://en.wikipedia.org/wiki/Monte_Carlo_method)으로 `pi`값을 추정해 보기. (`Pool`, `numpy` 사용)
복잡도에 대해 잘 알려진 문제이고, 쉽게 parallelize될 수 있음.

- thread로 numpy를 사용하여 구현.
- Pool을 사용해서 구현.


## Estimating Pi Using the Monte Carlo Method

### No use `multiprocessing` (named "Series"), Using threads, Using processes
