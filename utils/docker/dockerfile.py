from dto.controllers.image import Layer, DockerfileInstruction


def create_dockerfile(super_image: str, layers: list[Layer]) -> str:
    dockerfile_lines = []

    dockerfile_lines.append(f"{DockerfileInstruction.FROM.value} {super_image}")
    command_lines_joiner = " && \\\n\t"
    for layer in layers:
        instruction_line = f"{layer.instruction.value} {command_lines_joiner.join(layer.command_arguments)}"

        if layer.description:
            instruction_line += f"  # {layer.description}"

        dockerfile_lines.append(instruction_line)

    dockerfile_content = "\n".join(dockerfile_lines)

    return dockerfile_content
