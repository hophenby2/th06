// Locate and decompile functions that reference every requested scalar.
//@category TH062.Research

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.scalar.Scalar;

public class DecompileFunctionsWithScalars extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length == 0) {
            throw new IllegalArgumentException("pass one or more integer/hex scalar values");
        }

        Set<Long> wanted = new LinkedHashSet<>();
        for (String arg : args) {
            wanted.add(Long.decode(arg));
        }

        Map<Function, Set<Long>> matches = new LinkedHashMap<>();
        InstructionIterator instructions = currentProgram.getListing().getInstructions(true);
        while (instructions.hasNext() && !monitor.isCancelled()) {
            Instruction instruction = instructions.next();
            Function function = currentProgram.getFunctionManager().getFunctionContaining(
                instruction.getAddress()
            );
            if (function == null) {
                continue;
            }
            for (int operandIndex = 0; operandIndex < instruction.getNumOperands(); operandIndex++) {
                for (Object object : instruction.getOpObjects(operandIndex)) {
                    if (!(object instanceof Scalar)) {
                        continue;
                    }
                    long value = ((Scalar) object).getUnsignedValue();
                    if (wanted.contains(value)) {
                        matches.computeIfAbsent(function, unused -> new LinkedHashSet<>()).add(value);
                    }
                }
            }
        }

        List<Function> selected = new ArrayList<>();
        for (Map.Entry<Function, Set<Long>> entry : matches.entrySet()) {
            if (entry.getValue().containsAll(wanted)) {
                selected.add(entry.getKey());
            }
        }

        println("MATCHING_FUNCTIONS=" + selected.size());
        DecompInterface decompiler = new DecompInterface();
        decompiler.toggleCCode(true);
        decompiler.toggleSyntaxTree(false);
        if (!decompiler.openProgram(currentProgram)) {
            throw new IllegalStateException("failed to open program in decompiler");
        }
        try {
            for (Function function : selected) {
                println("===== " + function.getName() + " @ " + function.getEntryPoint() + " =====");
                DecompileResults result = decompiler.decompileFunction(function, 120, monitor);
                if (!result.decompileCompleted()) {
                    println("DECOMPILE_FAILED: " + result.getErrorMessage());
                    continue;
                }
                println(result.getDecompiledFunction().getC());
            }
        }
        finally {
            decompiler.dispose();
        }
    }
}
