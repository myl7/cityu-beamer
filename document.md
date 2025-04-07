# 改进 SimpleFact (Improving SimpleFact)

## Basic Idea of Finetuning

- We finetune Qwen to avoid hallucinated responses.
   - **Generate more factual and consistent answers**: If the model can give correct answers 4 out of 10 times, we want it to output correct answers 10 out of 10 times
   - **Acknowledge when unable to answer correctly**: If the model gives incorrect answers consistently, we want it to output "I don't know"

### Setup

- **Training Dataset**: As SimpleQA is too difficult, we mixed SimpleQA, PopQA, SelfAware, and TriviaQA **evenly**.
- **Model**: Qwen32B 2.5 with LoRA Training
- **Predefined Instruction**: A cold start prompt is used to induce reasoning and refusal capability.

> **System prompt:** A conversation between User and Assistant. The Assistant must think step by step. Then give a brief answer in \boxed{} if sure about the answer, otherwise the Assistant can return \boxed{Unknown} if not sure.

## Design Training Objective

### Rewards

- We use **reinforcement learning (RL)**, which trains a model to maximize given rewards.
- The reward function both encourages factual accuracy and reduces hallucination.
- Consider at each training step, when the model generates 20 responses:
   - **If any response is correct**: the **correct** response gets 1 reward, **process-correct** gets 0.5, and others get 0 (The model should answer correctly)
   - **If none are correct**: **not-attempting** responses get 1 score and others get 0. (When the model is unlikely to be correct, it should not attempt answering)

### RL Goal

- We use GRPO (Generalized Reward-weighted Posterior Optimization, the algorithm used for training Deepseek R1 to reason)

![grpo_visual.png](https://res.craft.do/user/full/8b9fa3b1-1b5d-02d9-76ce-dc44d8785d4a/doc/1E91F4BC-4955-4311-9683-7FFA57EEA174/D5F73D25-3755-4184-ABE1-593CEDEEF47B_2/8PVoVvkYAZokgtcT7cSr5pmJUckNRppmikfJWuqp7U0z/grpo_visual.png)

## GPRO Results

- Training is very noisy:

![Image](https://res.craft.do/user/full/8b9fa3b1-1b5d-02d9-76ce-dc44d8785d4a/doc/1E91F4BC-4955-4311-9683-7FFA57EEA174/C5ECB186-B75A-4C7E-9FDA-EB20789BF3FB_2/YDEZ7nAS8z7a1nkfIc0086WK0kVqwuGbDwa5P6lBwz0z/Image.heic)

- But the rewards on evaluation dataset are increasing steadily:

![Image](https://res.craft.do/user/full/8b9fa3b1-1b5d-02d9-76ce-dc44d8785d4a/doc/1E91F4BC-4955-4311-9683-7FFA57EEA174/427817C2-0098-491A-BA64-4982D14C05D0_2/89dbatS5VAqPvOofgULF80akUP2nmLJlQteeAQwdLYcz/Image.heic)

- Evaluation results decomposition:

| **Training Steps** | **Partial Correct** | **Partial NotAttempt** | **All NotAttempt** | **All Correct** | **All Attempt and Wrong** |
| ------------------ | ------------------- | ---------------------- | ------------------ | --------------- | ------------------------- |
| 200                | 36.67               | 33.33                  | 8.33               | 10.00           | 11.67                     |
| 400                | 33.33               | 33.33                  | 10.00              | 10.00           | 13.33                     |
| 600                | 30.00               | 33.33                  | 13.33              | 10.00           | 13.33                     |
| 800                | 31.67               | 35.00                  | 11.67              | 10.00           | 11.67                     |
| 1000               | 26.67               | 28.33                  | 20.00              | 13.33           | 11.67                     |
| 1200               | 25.00               | 30.00                  | 21.67              | 13.33           | 10.00                     |

### Observations

- The model does not deviate significantly from the original model (small KL divergence)
- Reward has high variance (many 0s, many 1s across the training session)
- Model learned to not attempt questions in both "Partial Correct" and "Partial Not Attempt" categories.
   - **We actually don't want "Partial Correct" to drop**

## Problems

- Too many training samples that are either too easy or too hard
- Didn't observe long reasoning or emerging behavior, although rewards are increasing
- Full training on 7B model encounters NaN values
- The system prompt is too simple
- Model prioritizes not attempting answers even for simple questions
- Training takes too much time (**33 hours**)

## Second Round Improvement

- Try different system prompts for a better starting point
- Filter the training set to exclude trivial or impossible samples
- Add KL clipping to stabilize 7B full training
- Apply fact and caution rewards separately
   - To analyze how each reward component is working

### Filtering Training Data

- Too many trivial or impossible samples (evident by frequency of 0 and 1 rewards)
- A sample is **just-hard-enough** if the model only generates correct answers sometimes
- Use original model to predict each sample 16 times
- Filter to keep top 2500 samples with most varied outputs

### Use Different System Prompts

- We find **system prompts** greatly affect model behavior
- If we encourage the model to be cautious, it will have more "NotAttempt" responses and fewer correct answers
- Experimenting with different prompts reveals a trade-off boundary
- We chose a balanced prompt for training

![Image.png](https://res.craft.do/user/full/8b9fa3b1-1b5d-02d9-76ce-dc44d8785d4a/doc/1E91F4BC-4955-4311-9683-7FFA57EEA174/36D6A4BC-F329-40DC-9DD3-DC2CF9CFBA42_2/cz6V6tOy7csEsw8ollDVJRrmGyMx7CAypV744ZWdDkoz/Image.png)

### Use 7B Full Training

- 32B + LoRA allows us to use a stronger base model, but has limitations:
   - Slower to train
   - Less optimization freedom (LoRA only updates a small subset of model parameters)
- Benefits of 7B Full Training:
   - In PPO methods like GRPO, we can enable policy clipping to prevent excessive model updates in one step, stabilizing training
   - 7B model takes 7 hours for one epoch instead of 33 hours

## Second Round Results

### Setup

- We tested 4 settings:
   - Only use fact reward
   - Only use caution reward
   - Use fact and caution rewards simultaneously
   - First apply fact reward, then caution reward
- Reasoning: (1) Training is not stable when two rewards are applied simultaneously; (2) Caution is easier to learn than factuality

### Results

- The 7B models can also benefit from RL training
- The fact and caution rewards seem to conflict with each other
- The model prioritizes "NotAttempt" responses
- RL can push the performance frontier, but not drastically

## Next Steps

- Make reasonable efforts to further improve results
- Draft the paper
   - Instead of focusing solely on better accuracy
   - Focus on balancing correctness and caution

