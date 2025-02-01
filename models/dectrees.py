from sklearn.tree import DecisionTreeClassifier

from models.base_model import BaseModel

class DecTrees(BaseModel):
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
        optionally min_samples_split (default: None so in-built)
            What is it
                Definition: The minimum number of samples required to split an internal node.
                Purpose: Prevents the tree from splitting a node if there aren't enough samples to justify it.
                Default Value: 2 (node can split as long as it has 2 or more samples).
            Why it matters
                Higher values: Creates fewer splits, resulting in a simpler tree and reduced overfitting.
                Lower values: Allows more splits, potentially increasing overfitting.
        optionally min_samples_leaf (default: None so in-built)
            What is it
                Definition: The minimum number of samples that must be present in a leaf node.
                Purpose: Ensures that leaf nodes have a minimum number of samples to prevent overly specific splits.
                Default Value: 1 (a leaf node can contain a single sample).
            Why it matters
                Higher values: Forces leaf nodes to represent a larger portion of the data, leading to a simpler and more generalized tree.
                Lower values: Allows leaf nodes with fewer samples, increasing the risk of overfitting.
    Calculates: model
    '''
    def fit(self, max_depth=None, min_samples_split=2, min_samples_leaf=1):
        self.model = DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, random_state=42)
        self.model.fit(self.X_train, self.Y_train)
