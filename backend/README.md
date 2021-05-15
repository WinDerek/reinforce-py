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

## 2. Other environments

**Tensorflow environment**

```shell
$ conda create --name tensorflow_env python=3.8
$ conda activate tensorflow_env
$ conda install pip
$ pip install tensorflow==${version}
```

Here I set the TensorFlow version as `2.3.0` because the cuda version on my machine is `10.1` and the latest TensorFlow version supporting it is `2.3.0` according to [this page](https://www.tensorflow.org/install/source#gpu).

**Tianshou environment**

```shell
$ conda create --name tianshou_env python=3.8
$ conda activate tianshou_env
$ conda install pip
$ pip install tianshou
```

`tianshou_test.py`

**Ray RLlib**

```shell
$ conda create --name rllib_env python=3.8
$ conda activate rllib_env
$ conda install pip
$ pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio===0.7.2 -f https://download.pytorch.org/whl/torch_stable.html # Install PyTorch
$ pip install ray==1.1.0 # Install Ray
$ pip install 'ray[rllib]==1.1.0' # Install RLlib
$ pip install tensorboard==2.4.0 # Install TensorBoard
$ LD_LIBRARY_PATH=/home/derek/.mujoco/mujoco200/bin pip install mujoco-py==2.0.2.13 # Install mujoco-py, and perform the setup instructions here: https://github.com/openai/mujoco-py/
```

Clear this conda environment:

```shell
$ conda remove --name rllib_env --all
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
