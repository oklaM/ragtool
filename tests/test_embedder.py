import unittest
from unittest.mock import patch, MagicMock
from core.embedder import OpenAIEmbedder, SentenceTransformerEmbedder, get_embedder
from core import constants

class TestEmbedder(unittest.TestCase):

    @patch('core.embedder.openai')
    def test_openai_embedder(self, mock_openai):
        mock_embedding = {
            'data': [
                {
                    'embedding': [0.1, 0.2, 0.3]
                }
            ]
        }
        mock_openai.Embedding.create.return_value = mock_embedding

        embedder = OpenAIEmbedder(model_name='text-embedding-3-small', api_key='test_key')
        embedding = embedder.embed(['test text'])

        self.assertEqual(embedding, [[0.1, 0.2, 0.3]])
        mock_openai.Embedding.create.assert_called_once_with(input=['test text'], model='text-embedding-3-small')

    @patch('core.embedder.SentenceTransformer')
    def test_sentence_transformer_embedder(self, mock_sentence_transformer):
        mock_model = MagicMock()
        mock_model.encode.return_value = [[0.4, 0.5, 0.6]]
        mock_sentence_transformer.return_value = mock_model

        embedder = SentenceTransformerEmbedder(model_name='all-MiniLM-L6-v2')
        embedding = embedder.embed(['test text'])

        self.assertEqual(embedding, [[0.4, 0.5, 0.6]])
        mock_model.encode.assert_called_once_with(['test text'], show_progress_bar=False)

    def test_get_embedder_openai(self):
        config = {
            constants.EMBEDDING: {
                constants.PROVIDER: constants.PROVIDER_OPENAI,
                constants.MODEL: 'text-embedding-3-small',
                constants.API_KEY: 'test_key'
            }
        }
        embedder = get_embedder(config)
        self.assertIsInstance(embedder, OpenAIEmbedder)

    def test_get_embedder_sentence_transformer(self):
        config = {
            constants.EMBEDDING: {
                constants.PROVIDER: constants.PROVIDER_SENTENCE_TRANSFORMERS,
                constants.MODEL: 'all-MiniLM-L6-v2'
            }
        }
        embedder = get_embedder(config)
        self.assertIsInstance(embedder, SentenceTransformerEmbedder)

    def test_get_embedder_auto_openai(self):
        config = {
            constants.EMBEDDING: {
                constants.PROVIDER: constants.PROVIDER_AUTO,
                constants.MODEL: 'text-embedding-3-small',
                constants.API_KEY: 'test_key'
            }
        }
        embedder = get_embedder(config)
        self.assertIsInstance(embedder, OpenAIEmbedder)

    def test_get_embedder_auto_sentence_transformer(self):
        config = {
            constants.EMBEDDING: {
                constants.PROVIDER: constants.PROVIDER_AUTO,
                constants.MODEL: 'all-MiniLM-L6-v2'
            }
        }
        embedder = get_embedder(config)
        self.assertIsInstance(embedder, SentenceTransformerEmbedder)

if __name__ == '__main__':
    unittest.main()
