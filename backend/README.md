# Backend

## 1. Setup the conda environment

```shell
$ conda create --name reinforce_py_env
$ conda activate reinforce_py_env
$ conda install pip
$ pip install scipy
$ pip install matplotlib
$ pip install Flask==1.1.2
$ pip install -U flask-cors
$ pip install jupyterlab
```

**Tensorflow Environment**

```shell
$ conda create --name tensorflow_env python=3.8
$ conda activate tensorflow_env
$ conda install pip
$ pip install tensorflow
```

## 2. Experiments

### 2.1 DBS value iteration

```shell
$ bash run_dbs_value_iteration.sh
```

### 2.2 DBS Q-learning

[TODO]

```shell
$ bash run_dbs_q_learning.sh
```

### 2.3 DBS DQN

[TODO]

```shell
$ bash run_dbs_dqn.sh
```
