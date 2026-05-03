"""Tests for abstraction_planes plane analyzer."""

import json
import pytest
from unittest.mock import patch, MagicMock
from abstraction_planes import (
    PLANES, FLUX_OPS, decompose, evaluate_quality, find_optimal_plane
)


class TestPlanes:
    """Test plane definitions."""

    def test_planes_has_six_entries(self):
        assert len(PLANES) == 6

    def test_planes_keys_range_0_to_5(self):
        assert sorted(PLANES.keys()) == [0, 1, 2, 3, 4, 5]

    def test_plane_5_is_intent(self):
        assert "Intent" in PLANES[5]

    def test_plane_0_is_bare_metal(self):
        assert "Bare Metal" in PLANES[0]

    def test_plane_4_is_domain_language(self):
        assert "Domain Language" in PLANES[4]

    def test_plane_3_is_structured_ir(self):
        assert "Structured IR" in PLANES[3]


class TestFluxOps:
    """Test FLUX opcode definitions."""

    def test_flux_ops_has_required_opcodes(self):
        required = ["MOVI", "MOV", "IADD", "JMP", "HALT", "ALERT"]
        for op in required:
            assert op in FLUX_OPS

    def test_flux_ops_are_hex_strings(self):
        for op, code in FLUX_OPS.items():
            assert code.startswith("0x")
            assert len(code) == 4

    def test_flux_ops_opcode_count(self):
        assert len(FLUX_OPS) >= 14


class TestDecompose:
    """Test decomposition logic."""

    def test_decompose_5_to_4_returns_tuple(self):
        with patch('abstraction_planes.call_qwen', return_value=("test output", 50)):
            result = decompose("test intent", 5, 4)
            assert isinstance(result, tuple)
            assert len(result) == 2

    def test_decompose_3_to_2_uses_deepseek(self):
        with patch('abstraction_planes.call_deepseek', return_value=("hex output", 30)):
            result = decompose("test intent", 3, 2)
            assert "hex output" in result

    def test_decompose_unknown_plane_uses_deepseek(self):
        with patch('abstraction_planes.call_deepseek', return_value=("unknown plane result", 15)):
            result = decompose("test intent", 0, -1)
            assert result[0] == "unknown plane result"

    @patch('abstraction_planes.call_qwen')
    def test_decompose_prompts_have_plane_transitions(self, mock_qwen):
        mock_qwen.return_value = ("output", 10)
        decompose("test", 5, 4)
        # Verify prompt includes FLUX-ese
        assert mock_qwen.call_args[0][0] == "Convert this natural language intent into FLUX-ese domain language (structured maritime-style notation): test"


class TestEvaluateQuality:
    """Test quality evaluation."""

    def test_evaluate_quality_returns_dict(self):
        with patch('abstraction_planes.call_deepseek', return_value=('{"correctness": 8, "compactness": 7, "executability": 6, "maintainability": 9}', 50)):
            result = evaluate_quality("original", "decomposed", 4)
            assert isinstance(result, dict)

    def test_evaluate_quality_has_total_score(self):
        with patch('abstraction_planes.call_deepseek', return_value=('{"correctness": 8, "compactness": 7, "executability": 6, "maintainability": 9}', 50)):
            result = evaluate_quality("original", "decomposed", 4)
            assert "total" in result

    def test_evaluate_quality_fallback_on_invalid_json(self):
        with patch('abstraction_planes.call_deepseek', return_value=('not json at all', 30)):
            result = evaluate_quality("original", "decomposed", 4)
            assert result["total"] == 5.0
            assert "correctness" in result

    def test_evaluate_quality_extracts_json_from_text(self):
        with patch('abstraction_planes.call_deepseek', return_value=('Here is the JSON: {"correctness": 7, "compactness": 8, "executability": 9, "maintainability": 6}', 60)):
            result = evaluate_quality("original", "decomposed", 3)
            assert result["correctness"] == 7


class TestFindOptimalPlane:
    """Test optimal plane finding."""

    @patch('abstraction_planes.decompose')
    @patch('abstraction_planes.evaluate_quality')
    @patch('time.sleep')
    def test_find_optimal_plane_returns_dict(self, mock_sleep, mock_eval, mock_decomp):
        mock_decomp.return_value = ("decomposed", 50)
        mock_eval.return_value = {"correctness": 7, "compactness": 7, "executability": 7, "maintainability": 7, "total": 7}
        
        result = find_optimal_plane("navigate east 10 knots")
        assert isinstance(result, dict)
        assert "optimal_plane" in result

    @patch('abstraction_planes.decompose')
    @patch('abstraction_planes.evaluate_quality')
    @patch('time.sleep')
    def test_esp32_target_floors_at_0(self, mock_sleep, mock_eval, mock_decomp):
        mock_decomp.return_value = ("output", 30)
        mock_eval.return_value = {"correctness": 6, "compactness": 6, "executability": 6, "maintainability": 6, "total": 6}
        
        result = find_optimal_plane("sensor reading", target="esp32")
        assert result["optimal_plane"] <= 0

    @patch('abstraction_planes.decompose')
    @patch('abstraction_planes.evaluate_quality')
    @patch('time.sleep')
    def test_cloud_target_floors_at_3(self, mock_sleep, mock_eval, mock_decomp):
        mock_decomp.return_value = ("output", 30)
        mock_eval.return_value = {"correctness": 6, "compactness": 6, "executability": 6, "maintainability": 6, "total": 6}
        
        result = find_optimal_plane("fleet coordination", target="cloud")
        assert result["optimal_plane"] >= 3

    @patch('abstraction_planes.decompose')
    @patch('abstraction_planes.evaluate_quality')
    @patch('time.sleep')
    def test_diminishing_returns_stops_early(self, mock_sleep, mock_eval, mock_decomp):
        mock_decomp.return_value = ("output", 30)
        # Negative improvement should trigger stop
        mock_eval.side_effect = [
            {"correctness": 8, "compactness": 8, "executability": 8, "maintainability": 8, "total": 8},
            {"correctness": 5, "compactness": 5, "executability": 5, "maintainability": 5, "total": 5},  # -3 improvement
        ]
        
        result = find_optimal_plane("test intent", target="auto")
        # Should stop at plane 4 (before the negative drop)
        assert result["optimal_plane"] >= 4

    @patch('abstraction_planes.decompose')
    @patch('abstraction_planes.evaluate_quality')
    @patch('time.sleep')
    def test_result_includes_target(self, mock_sleep, mock_eval, mock_decomp):
        mock_decomp.return_value = ("output", 30)
        mock_eval.return_value = {"correctness": 7, "compactness": 7, "executability": 7, "maintainability": 7, "total": 7}
        
        result = find_optimal_plane("test", target="jetson")
        assert result["target"] == "jetson"

    @patch('abstraction_planes.decompose')
    @patch('abstraction_planes.evaluate_quality')
    @patch('time.sleep')
    def test_result_includes_scores(self, mock_sleep, mock_eval, mock_decomp):
        mock_decomp.return_value = ("output", 30)
        mock_eval.return_value = {"correctness": 7, "compactness": 8, "executability": 6, "maintainability": 9, "total": 7.5}
        
        result = find_optimal_plane("test")
        assert "scores" in result


class TestTargetFloors:
    """Test target-based floor logic via find_optimal_plane."""

    @patch('abstraction_planes.decompose')
    @patch('abstraction_planes.evaluate_quality')
    @patch('time.sleep')
    def test_mud_target_floor(self, mock_sleep, mock_eval, mock_decomp):
        mock_decomp.return_value = ("output", 30)
        mock_eval.return_value = {"correctness": 6, "compactness": 6, "executability": 6, "maintainability": 6, "total": 6}
        
        result = find_optimal_plane("test", target="mud")
        assert result["optimal_plane"] >= 2

    @patch('abstraction_planes.decompose')
    @patch('abstraction_planes.evaluate_quality')
    @patch('time.sleep')
    def test_agent_target_floor(self, mock_sleep, mock_eval, mock_decomp):
        mock_decomp.return_value = ("output", 30)
        mock_eval.return_value = {"correctness": 6, "compactness": 6, "executability": 6, "maintainability": 6, "total": 6}
        
        result = find_optimal_plane("test", target="agent")
        assert result["optimal_plane"] >= 3


class TestIntegration:
    """Integration-style tests that don't hit real APIs."""

    @patch('abstraction_planes.call_deepseek')
    @patch('abstraction_planes.call_qwen')
    @patch('time.sleep')
    def test_full_decomposition_chain(self, mock_sleep, mock_qwen, mock_deepseek):
        mock_qwen.return_value = ("flux-ese output", 40)
        mock_deepseek.return_value = ("hex bytecode", 60)
        
        # Decompose 5->4
        r1, t1 = decompose("test intent", 5, 4)
        assert r1 == "flux-ese output"
        
        # Decompose 4->3
        r2, t2 = decompose("flux-ese output", 4, 3)
        # Uses deepseek for lower planes

    def test_planes_constant_values(self):
        """Verify plane descriptions are meaningful."""
        assert len(PLANES[5]) > 10  # Intent description not empty
        assert len(PLANES[0]) > 10  # Bare metal description not empty

    def test_all_planes_have_descriptions(self):
        """Every plane should have a non-empty description."""
        for plane in range(6):
            assert plane in PLANES
            assert len(PLANES[plane]) > 5

    def test_flux_ops_hex_format(self):
        """All FLUX ops should be valid hex format."""
        for op, code in FLUX_OPS.items():
            # Should be 0xNN format
            assert code.startswith("0x")
            int_val = int(code, 16)
            assert 0 <= int_val <= 0xFF