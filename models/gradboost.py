from sklearn.ensemble import GradientBoostingClassifier

class GradBoostMachines(BaseModel):
    '''
    Takes:
        optionally max_depth (default: None)
        What is it
            Definition: The maximum depth of the decision tree. Depth is the number of splits from the root node to the deepest leaf node.
            Purpose: Controls the maximum number of levels in the tree, limiting its complexity.
            Default Value: If not set, the tree will grow until all leaves are pure (or until min_samples_split or min_samples_leaf stops further splitting).
        Why it matters
            Deeper trees: More complex, can model intricate patterns but may overfit the training data.
            Shallow trees: Simpler, may underfit the data and fail to capture important relationships.
        optionally min_samples_split (default: 2)
        What is it
            Definition: The minimum number of samples required to split an internal node.
            Purpose: Prevents the tree from splitting a node if there aren't enough samples to justify it.
            Default Value: 2 (node can split as long as it has 2 or more samples).
        Why it matters
            Higher values: Creates fewer splits, resulting in a simpler tree and reduced overfitting.
            Lower values: Allows more splits, potentially increasing overfitting.
        optionally min_samples_leaf (default: 1)
        What is it
            Definition: The minimum number of samples that must be present in a leaf node.
            Purpose: Ensures that leaf nodes have a minimum number of samples to prevent overly specific splits.
            Default Value: 1 (a leaf node can contain a single sample).
        Why it matters
            Higher values: Forces leaf nodes to represent a larger portion of the data, leading to a simpler and more generalized tree.
            Lower values: Allows leaf nodes with fewer samples, increasing the risk of overfitting.
        optionally n_estimators (default: 100)
        What is it
            Definition: The number of boosting stages (trees) to be used.
            Purpose: Controls the number of sequential trees that are added to the model. A higher value means more trees are included, which can improve accuracy but
                    also increase computation.
            Default Value: 100.
        Why it matters
            More Trees:
            Increased accuracy: More trees provide more chances to correct errors made by previous trees, potentially leading to better overall performance.
            Increased computational cost: Training and predicting with more trees require more resources (time and memory), and this can slow down the process, especially
                                            with large datasets.
            Decreased marginal returns: After a certain point, adding more trees provides diminishing returns in terms of accuracy. A very large number of trees can result
                                        in overfitting.
            Fewer Trees:
            Faster computation: Fewer trees will result in a quicker model training and prediction process, which can be useful for large datasets or when computational
                                efficiency is a concern.
            Potential underfitting: If too few trees are used, the model may not have enough capacity to capture the complexities in the data, leading to lower accuracy
                                    and poorer performance.
        optionally learning_rate (default: 0.1)
        What is it
            Definition: The step size at each iteration while moving toward a minimum of the loss function. It controls the contribution of each individual tree to the final
                        prediction.
            Purpose: Controls how much each tree corrects the previous tree's errors. Smaller learning rates result in slower learning but may lead to better generalization
                    and performance when paired with more trees.
            Default Value: 0.1.
        Why it matters
            Smaller Learning Rate:
            More trees needed: A smaller learning rate requires a larger number of trees to reach the same level of accuracy, since each tree contributes less to the final model.
            Better generalization: Smaller learning rates typically help prevent overfitting and allow the model to learn more gradually, which can improve generalization to unseen data.
            Decreased speed: With smaller learning rates, training will take longer, as you need more trees to achieve the same effect.
            Larger Learning Rate:
            Faster convergence: Larger values allow the model to converge more quickly, but this can lead to overfitting as the model may become too aggressive in adapting to the training data.
            Risk of underfitting: If the learning rate is too high, the model might skip over optimal solutions, leading to poor performance.
    Calculates: X_train, X_test, Y_train, Y_test, model
    '''
    def fit(self, max_depth=None, min_samples_split=2, min_samples_leaf=1, n_estimators=200, learning_rate=0.1):
        self.model = GradientBoostingClassifier(n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, learning_rate=learning_rate, random_state=42)
        self.model.fit(self.X_train, self.Y_train)
