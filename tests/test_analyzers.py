"""
Tests for analyzer modules
"""
import pytest
from pathlib import Path
import tempfile
import os

from src.analyzers.entropy_analyzer import analyze_file as analyze_entropy
from src.analyzers.pe_analyzer import analyze_file as analyze_pe
from src.utils.hash import compute_hashes


class TestEntropyAnalyzer:
    def test_entropy_low(self):
        """Test entropy analysis on low-entropy file"""
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
            # Write repetitive data (low entropy)
            f.write(b'A' * 1000)
            temp_path = f.name
        
        try:
            result = analyze_entropy(temp_path)
            assert 'entropy' in result
            assert result['entropy'] < 1.0  # Very low entropy
        finally:
            os.unlink(temp_path)
    
    def test_entropy_high(self):
        """Test entropy analysis on high-entropy file"""
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
            # Write random data (high entropy)
            f.write(os.urandom(1000))
            temp_path = f.name
        
        try:
            result = analyze_entropy(temp_path)
            assert 'entropy' in result
            assert result['entropy'] > 7.0  # High entropy
        finally:
            os.unlink(temp_path)
    
    def test_entropy_nonexistent_file(self):
        """Test entropy analysis on non-existent file"""
        result = analyze_entropy('/nonexistent/file.txt')
        assert 'entropy_error' in result


class TestPEAnalyzer:
    def test_non_pe_file(self):
        """Test PE analysis on non-PE file"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='wb') as f:
            f.write(b'Not a PE file')
            temp_path = f.name
        
        try:
            result = analyze_pe(temp_path)
            assert result['is_pe'] == False
        finally:
            os.unlink(temp_path)
    
    def test_pe_file_extension_check(self):
        """Test that PE analyzer checks file extensions"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.exe', mode='wb') as f:
            f.write(b'MZ')  # PE header start
            temp_path = f.name
        
        try:
            result = analyze_pe(temp_path)
            # Should attempt PE analysis due to .exe extension
            assert 'is_pe' in result
        finally:
            os.unlink(temp_path)


class TestHashUtility:
    def test_hash_computation(self):
        """Test hash computation"""
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
            f.write(b'Test content for hashing')
            temp_path = f.name
        
        try:
            result = compute_hashes(temp_path, ('sha256',))
            assert 'sha256' in result
            assert len(result['sha256']) == 64  # SHA256 hex length
        finally:
            os.unlink(temp_path)
    
    def test_hash_nonexistent_file(self):
        """Test hash computation on non-existent file"""
        result = compute_hashes('/nonexistent/file.txt', ('sha256',))
        assert 'error' in result
    
    def test_multiple_algorithms(self):
        """Test multiple hash algorithms"""
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
            f.write(b'Test content')
            temp_path = f.name
        
        try:
            result = compute_hashes(temp_path, ('sha256', 'md5', 'sha1'))
            assert 'sha256' in result
            assert 'md5' in result
            assert 'sha1' in result
            assert len(result['sha256']) == 64
            assert len(result['md5']) == 32
            assert len(result['sha1']) == 40
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
