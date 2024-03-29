FROM jupyter/base-notebook:latest

# enable jupyterlab as default app
ENV JUPYTER_ENABLE_LAB true

# install env with conda
COPY requirements.txt .
RUN conda config --add channels conda-forge && \
  conda install -y mamba && \
  mamba env update -n base -f ./requirements.txt && \
  conda clean -tipy && \
  fix-permissions $CONDA_DIR && \
  fix-permissions /home/$NB_USER
